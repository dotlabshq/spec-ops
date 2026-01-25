#!/usr/bin/env bash
# Common utilities for SpecOps scripts

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in a git repository
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        log_error "Not a git repository. Please run 'git init' first."
        return 1
    fi
    return 0
}

# Get the root directory of the git repository
get_git_root() {
    git rev-parse --show-toplevel
}

# Get the .specops directory path
get_specops_dir() {
    local git_root
    git_root=$(get_git_root)
    echo "${git_root}/.specops"
}

# Check if .specops directory exists
check_specops_dir() {
    local specops_dir
    specops_dir=$(get_specops_dir)
    
    if [[ ! -d "${specops_dir}" ]]; then
        log_error ".specops directory not found. Is this a SpecOps project?"
        return 1
    fi
    return 0
}

# Get current feature ID from git branch or environment variable
get_current_feature() {
    # Check environment variable first
    if [[ -n "${SPECOPS_FEATURE:-}" ]]; then
        echo "${SPECOPS_FEATURE}"
        return 0
    fi
    
    # Try to get from git branch
    if check_git_repo; then
        local branch
        branch=$(git rev-parse --abbrev-ref HEAD)
        
        # Extract feature ID from branch name (e.g., 001-sso-deployment -> 001-sso-deployment)
        if [[ "${branch}" =~ ^[0-9]{3}- ]]; then
            echo "${branch}"
            return 0
        fi
    fi
    
    log_error "Could not determine current feature. Set SPECOPS_FEATURE or use a feature branch."
    return 1
}

# Get the next feature ID
get_next_feature_id() {
    local specops_dir
    specops_dir=$(get_specops_dir)
    local specs_dir="${specops_dir}/specs"
    
    # Create specs directory if it doesn't exist
    mkdir -p "${specs_dir}"
    
    # Find the highest existing feature ID
    local max_id=0
    for dir in "${specs_dir}"/[0-9][0-9][0-9]-*; do
        if [[ -d "${dir}" ]]; then
            local id
            id=$(basename "${dir}" | cut -d'-' -f1)
            if [[ ${id} -gt ${max_id} ]]; then
                max_id=${id}
            fi
        fi
    done
    
    # Return next ID with leading zeros
    printf "%03d" $((max_id + 1))
}

# Create feature directory structure
create_feature_dir() {
    local feature_id="$1"
    local specops_dir
    specops_dir=$(get_specops_dir)
    local feature_dir="${specops_dir}/specs/${feature_id}"
    
    if [[ -d "${feature_dir}" ]]; then
        log_warning "Feature directory already exists: ${feature_dir}"
        return 0
    fi
    
    mkdir -p "${feature_dir}"
    log_success "Created feature directory: ${feature_dir}"
}

# Check if a file exists
file_exists() {
    local file="$1"
    [[ -f "${file}" ]]
}

# Create a file from template
create_from_template() {
    local template="$1"
    local output="$2"
    
    if [[ ! -f "${template}" ]]; then
        log_error "Template not found: ${template}"
        return 1
    fi
    
    if [[ -f "${output}" ]]; then
        log_warning "File already exists: ${output}"
        return 0
    fi
    
    cp "${template}" "${output}"
    log_success "Created: ${output}"
}

# Ensure constitution exists
ensure_constitution() {
    local specops_dir
    specops_dir=$(get_specops_dir)
    local constitution="${specops_dir}/memory/constitution.md"
    
    if [[ ! -f "${constitution}" ]]; then
        log_error "Constitution not found. Please run /specops.constitution first."
        return 1
    fi
    return 0
}

# Ensure specification exists for current feature
ensure_specification() {
    local feature_id
    feature_id=$(get_current_feature) || return 1
    
    local specops_dir
    specops_dir=$(get_specops_dir)
    local spec="${specops_dir}/specs/${feature_id}/spec.md"
    
    if [[ ! -f "${spec}" ]]; then
        log_error "Specification not found for feature ${feature_id}. Please run /specops.specify first."
        return 1
    fi
    return 0
}

# Ensure plan exists for current feature
ensure_plan() {
    local feature_id
    feature_id=$(get_current_feature) || return 1
    
    local specops_dir
    specops_dir=$(get_specops_dir)
    local plan="${specops_dir}/specs/${feature_id}/plan.md"
    
    if [[ ! -f "${plan}" ]]; then
        log_error "Plan not found for feature ${feature_id}. Please run /specops.plan first."
        return 1
    fi
    return 0
}

# Ensure tasks exist for current feature
ensure_tasks() {
    local feature_id
    feature_id=$(get_current_feature) || return 1
    
    local specops_dir
    specops_dir=$(get_specops_dir)
    local tasks="${specops_dir}/specs/${feature_id}/tasks.md"
    
    if [[ ! -f "${tasks}" ]]; then
        log_error "Tasks not found for feature ${feature_id}. Please run /specops.tasks first."
        return 1
    fi
    return 0
}

# Export functions for use in other scripts
export -f log_info
export -f log_success
export -f log_warning
export -f log_error
export -f check_git_repo
export -f get_git_root
export -f get_specops_dir
export -f check_specops_dir
export -f get_current_feature
export -f get_next_feature_id
export -f create_feature_dir
export -f file_exists
export -f create_from_template
export -f ensure_constitution
export -f ensure_specification
export -f ensure_plan
export -f ensure_tasks