#!/usr/bin/env bash

set -euo pipefail

usage() {
	cat <<'EOF'
Usage:
  create-project.sh --type TYPE --name NAME [options]

Types:
	app, game, website, prestashop

Options:
  --components LIST  Comma-separated components for the project
  --path PATH        Explicit destination path; takes precedence over --root
  --root PATH        Development root (default: DEV_STANDARDS_DEVELOPMENT_ROOT or current directory)
	--owner OWNER      GitHub user or organization (default: authenticated user)
	--no-remote        Create only the local project; do not use GitHub
  --dry-run          Print the planned actions without changing files
  -h, --help         Show this help

Examples:
  create-project.sh --type app --name repost-app --components api,mobile,ios,android
	create-project.sh --type app --name repost-app --owner my-org
  create-project.sh --type game --name juego-movil --components ios,android --dry-run
EOF
}

fail() {
	printf 'Error: %s\n' "$1" >&2
	exit 1
}

project_type=""
project_name=""
components_csv=""
explicit_path=""
root_path=""
owner=""
create_remote=true
dry_run=false

while [[ $# -gt 0 ]]; do
	case "$1" in
		--type)
			[[ $# -ge 2 ]] || fail "--type requires a value"
			project_type="$2"
			shift 2
			;;
		--name)
			[[ $# -ge 2 ]] || fail "--name requires a value"
			project_name="$2"
			shift 2
			;;
		--components)
			[[ $# -ge 2 ]] || fail "--components requires a value"
			components_csv="$2"
			shift 2
			;;
		--path)
			[[ $# -ge 2 ]] || fail "--path requires a value"
			explicit_path="$2"
			shift 2
			;;
		--root)
			[[ $# -ge 2 ]] || fail "--root requires a value"
			root_path="$2"
			shift 2
			;;
		--owner)
			[[ $# -ge 2 ]] || fail "--owner requires a value"
			owner="$2"
			shift 2
			;;
		--no-remote)
			create_remote=false
			shift
			;;
		--dry-run)
			dry_run=true
			shift
			;;
		-h|--help)
			usage
			exit 0
			;;
		*)
			fail "unknown option: $1"
			;;
	esac
done

[[ -n "$project_type" ]] || fail "--type is required"
[[ -n "$project_name" ]] || fail "--name is required"
[[ "$project_name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]] || fail "project name must use lowercase kebab-case"
[[ ${#project_name} -le 100 ]] || fail "project name must be 100 characters or fewer"
case "$project_type" in
	app) category="apps"; allowed_components=" api web mobile ios android " ;;
	game) category="games"; allowed_components=" ios android " ;;
	website) category="websites"; allowed_components=" web " ;;
	prestashop) category="prestashop"; allowed_components=" " ;;
	*) fail "unsupported type: $project_type" ;;
esac

components=()
if [[ -n "$components_csv" ]]; then
	[[ "$project_type" != "prestashop" ]] || fail "type '$project_type' does not accept components"
	IFS=',' read -r -a requested_components <<< "$components_csv"
	seen_components=" "
	for component in "${requested_components[@]}"; do
		[[ -n "$component" ]] || fail "component list contains an empty value"
		case "$allowed_components" in
			*" $component "*) ;;
			*) fail "component '$component' is not valid for type '$project_type'" ;;
		esac
		case "$seen_components" in
			*" $component "*) fail "duplicate component: $component" ;;
		esac
		seen_components="${seen_components}${component} "
		components+=("$component")
	done
fi

gitignore_profiles=()
[[ "$project_type" != "website" ]] || gitignore_profiles+=(web)
if [[ ${#components[@]} -gt 0 ]]; then
	for component in "${components[@]}"; do
		case "$component" in
			web)
				[[ "$project_type" == "website" ]] || gitignore_profiles+=(web)
				;;
			ios) gitignore_profiles+=(ios) ;;
			android) gitignore_profiles+=(android) ;;
		esac
	done
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
standards_version="$(awk '$1 == "version:" { gsub(/"/, "", $2); print $2; exit }' "$repo_root/templates/project.yml")"
[[ -n "$standards_version" ]] || fail "could not read standards version from templates/project.yml"

if [[ -n "$explicit_path" ]]; then
	destination="$explicit_path"
else
	if [[ -z "$root_path" ]]; then
		root_path="${DEV_STANDARDS_DEVELOPMENT_ROOT:-$PWD}"
	fi
	destination="$root_path/$category/$project_name"
fi

case "$destination" in
	/*) ;;
	*) destination="$PWD/$destination" ;;
esac
while [[ "$destination" != "/" && "$destination" == */ ]]; do
	destination="${destination%/}"
done

[[ ! -e "$destination" ]] || fail "destination already exists: $destination"

remote_name=""
gh_command="$(command -v gh || true)"
if [[ -z "$gh_command" ]]; then
	for candidate in /opt/homebrew/bin/gh /usr/local/bin/gh; do
		if [[ -x "$candidate" ]]; then
			gh_command="$candidate"
			break
		fi
	done
fi

if [[ "$create_remote" == true && "$dry_run" == false ]]; then
	[[ -n "$gh_command" ]] || fail "GitHub CLI (gh) is required; authenticate it or use --no-remote"
	"$gh_command" auth status >/dev/null 2>&1 || fail "authenticate GitHub CLI with 'gh auth login' or use --no-remote"
	if [[ -z "$owner" ]]; then
		owner="$("$gh_command" api user --jq .login 2>/dev/null)" || fail "could not determine the authenticated GitHub user"
	fi
	[[ "$owner" =~ ^[A-Za-z0-9]([A-Za-z0-9-]{0,37}[A-Za-z0-9])?$ ]] || fail "owner must be a valid GitHub user or organization name"
	remote_name="$owner/$project_name"
	set +e
	remote_response="$("$gh_command" api --include "repos/$remote_name" 2>&1)"
	remote_status=$?
	set -e
	if [[ $remote_status -eq 0 ]]; then
		fail "GitHub repository already exists: $remote_name"
	fi
	case "$remote_response" in
		*"HTTP/2.0 404"*|*"HTTP/1.1 404"*|*"HTTP/3 404"*) ;;
		*) fail "could not verify GitHub repository availability for $remote_name; check access or use --no-remote" ;;
	esac
fi

if [[ "$dry_run" == true ]]; then
	printf 'Project type: %s\n' "$project_type"
	printf 'Project name: %s\n' "$project_name"
	if [[ ${#components[@]} -gt 0 ]]; then
		printf 'Components: %s\n' "$components_csv"
	else
		printf 'Components: none\n'
	fi
	printf 'Destination: %s\n' "$destination"
	printf 'Standards version: %s\n' "$standards_version"
	printf 'Would copy standards, generate project metadata, initialize Git, commit the scaffold, and create main/develop branches.\n'
	if [[ "$create_remote" == true ]]; then
		if [[ -n "$owner" ]]; then
			printf 'Would create private GitHub repository: %s/%s\n' "$owner" "$project_name"
		else
			printf 'Would create private GitHub repository for the authenticated user: %s\n' "$project_name"
		fi
	else
		printf 'No GitHub remote would be created.\n'
	fi
	exit 0
fi

command -v git >/dev/null 2>&1 || fail "git is required"
git config --global --get user.name >/dev/null 2>&1 || fail "set git user.name explicitly before creating a project"
git config --global --get user.email >/dev/null 2>&1 || fail "set git user.email explicitly before creating a project"

destination_parent="$(dirname "$destination")"
mkdir -p "$destination_parent"
temporary_project="$(mktemp -d "$destination_parent/.${project_name}.tmp.XXXXXX")"
cleanup() {
	if [[ -n "${temporary_project:-}" && -d "$temporary_project" ]]; then
		rm -rf "$temporary_project"
	fi
}
trap cleanup EXIT

mkdir -p "$temporary_project/.dev-standards/scripts" "$temporary_project/.github/prompts"
cp "$repo_root/templates/gitignore/common.gitignore" "$temporary_project/.gitignore"
if [[ ${#gitignore_profiles[@]} -gt 0 ]]; then
	for profile in "${gitignore_profiles[@]}"; do
		printf '\n' >> "$temporary_project/.gitignore"
		cat "$repo_root/templates/gitignore/$profile.gitignore" >> "$temporary_project/.gitignore"
	done
fi
cp "$repo_root/README.md" "$temporary_project/.dev-standards/README.md"
cp "$repo_root/GLOBAL.md" "$temporary_project/.dev-standards/GLOBAL.md"
cp -R "$repo_root/git" "$temporary_project/.dev-standards/git"
cp -R "$repo_root/prestashop" "$temporary_project/.dev-standards/prestashop"
cp -R "$repo_root/security" "$temporary_project/.dev-standards/security"
cp -R "$repo_root/testing" "$temporary_project/.dev-standards/testing"
cp -R "$repo_root/templates" "$temporary_project/.dev-standards/templates"
cp "$repo_root/scripts/create-project.sh" "$temporary_project/.dev-standards/scripts/create-project.sh"
chmod +x "$temporary_project/.dev-standards/scripts/create-project.sh"
cp -R "$repo_root/.github/prompts/." "$temporary_project/.github/prompts/"

{
	printf 'schema_version: 1\n\nproject:\n  name: %s\n  type: %s\n' "$project_name" "$project_type"
	if [[ ${#components[@]} -eq 0 ]]; then
		printf '  components: []\n'
	else
		printf '  components:\n'
		for component in "${components[@]}"; do
			printf '    - %s\n' "$component"
		done
	fi
	printf '\nstandards:\n  version: "%s"\n' "$standards_version"
} > "$temporary_project/.dev-standards/project.yml"

{
	printf '# %s\n\n' "$project_name"
	printf 'Tipo: `%s`\n\n' "$project_type"
	if [[ ${#components[@]} -gt 0 ]]; then
		printf 'Componentes: `%s`\n\n' "$components_csv"
	fi
	printf '## Desarrollo\n\nCompleta aquí las instrucciones para instalar, ejecutar y probar este proyecto.\n'
} > "$temporary_project/README.md"

{
	printf '# Contexto del proyecto\n\n'
	printf -- '- Nombre: `%s`\n- Tipo: `%s`\n' "$project_name" "$project_type"
	if [[ ${#components[@]} -gt 0 ]]; then
		printf -- '- Componentes: `%s`\n' "$components_csv"
	fi
	printf '\n## Propósito\n\nPendiente de definir.\n\n## Decisiones y restricciones\n\nPendiente de documentar.\n'
} > "$temporary_project/CONTEXT.md"

cat > "$temporary_project/AGENTS.md" <<'EOF'
# Instrucciones para agentes

- Lee `CONTEXT.md` y los estándares aplicables en `.dev-standards/` antes de cambiar código.
- Sigue `.dev-standards/GLOBAL.md` y el perfil correspondiente al tipo y componentes del proyecto.
- Redacta documentación, comentarios explicativos y textos visibles en español; usa inglés para identificadores internos y claves técnicas.
- No inventes requisitos ni decisiones de producto; consulta al mantenedor si falta información.
- Ejecuta las pruebas y comprobaciones pertinentes y resume sus resultados.
EOF

git -C "$temporary_project" init
git -C "$temporary_project" branch -M main
git -C "$temporary_project" add --all
git -C "$temporary_project" commit -m "Initialize project scaffold"
git -C "$temporary_project" checkout -b develop

if [[ -e "$destination" ]]; then
	fail "destination appeared during creation; temporary files will be removed: $destination"
fi
mv "$temporary_project" "$destination"
temporary_project=""
trap - EXIT

printf 'Created project: %s\n' "$destination"
printf 'Current branch: develop\n'
printf 'Standards version: %s\n' "$standards_version"

if [[ "$create_remote" == false ]]; then
	printf 'GitHub remote creation was skipped.\n'
	exit 0
fi

if ! "$gh_command" repo create "$remote_name" --private; then
	fail "local project remains at $destination; GitHub repository creation failed"
fi

if ! git -C "$destination" remote add origin "https://github.com/$remote_name.git"; then
	fail "GitHub repository was created, but origin could not be configured; local project remains at $destination"
fi

if ! git -C "$destination" push --set-upstream origin main || ! git -C "$destination" push --set-upstream origin develop; then
	fail "GitHub repository exists, but pushing branches failed; local project remains at $destination"
fi

printf 'GitHub repository created and main/develop pushed: %s\n' "$remote_name"

protection_payload='{"required_status_checks":null,"enforce_admins":false,"required_pull_request_reviews":null,"restrictions":null,"allow_force_pushes":false,"allow_deletions":false}'
if printf '%s' "$protection_payload" | gh api --method PUT "repos/$remote_name/branches/main/protection" --input - >/dev/null 2>&1; then
	printf 'Protected main against force-push and deletion.\n'
else
	printf 'Warning: GitHub did not apply branch protection. Protect main against force-push and deletion in repository settings.\n' >&2
fi