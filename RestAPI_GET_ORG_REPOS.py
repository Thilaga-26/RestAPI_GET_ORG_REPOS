""" Fetch repositories for a specific organization if the organization name is provided. 
If no organization name is provided, it will fetch repositories for all organizations 
associated with the GitHub account"""
import os
import argparse
import requests

# Retrieving GitHub access token from environment variable
access_token = os.environ.get("GITHUB_ACCESS_TOKEN")
if not access_token:
    print("GitHub access token not found. Please set the GITHUB_ACCESS_TOKEN environment variable.")

# Parsing command-line arguments
parser = argparse.ArgumentParser(description="Fetch repositories for a specific GitHub organization or all organizations")
parser.add_argument("--organization", help="Name of the organization")
args = parser.parse_args()

orgs_name = args.organization

def get_all_organizations(access_token):
    """
    This function retrieves names of all organizations from GitHub.

    Args:
        access_token (str): GitHub access token.

    Returns:
        list: Names of all organizations.
    """
    url_org = "https://api.github.com/user/orgs"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url_org, headers=headers)

    if response.status_code == 200:
        organizations = response.json()
        orgs_name = [org.get("login") for org in organizations]
        return orgs_name
    else:
        print("Failed to retrieve organizations. Status code:", response.status_code)
        return None

def get_repositories_for_organization(access_token, organization_name):
    """
    This function retrieves repositories for a specific organization from GitHub.

    Args:
        access_token (str): GitHub access token.
        organization_name (str): Name of the organization.

    Returns:
        list: Names of repositories for the organization.
    """
    url_repos = f"https://api.github.com/orgs/{organization_name}/repos"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url_repos, headers=headers)

    if response.status_code == 200:
        repository = response.json()
        repo_names = [repo.get("name") for repo in repository]
        return repo_names
    else:
        print(f"Failed to retrieve repositories for {organization_name}. Status code:",
              response.status_code)
        return None

# If organization name is provided, fetch repositories for that organization
if orgs_name:
    repositories = get_repositories_for_organization(access_token, orgs_name)
    # Displaying repositories names if found, otherwise printing a message
    if repositories:
        print(f"Repositories for organization '{orgs_name}':")
        for repo_name in repositories:
            print(repo_name)
    else:
        print(f"No repositories found for organization '{orgs_name}'.")

# If no organization name is provided, fetch repositories for all organizations
else:
    organization_names = get_all_organizations(access_token)
    # Displaying organization names if found, otherwise printing a message
    if organization_names:
        print("Fetching repositories for all organizations...")
        for org_name in organization_names:
            print(f"\nRepositories for organization '{org_name}':")
            repos = get_repositories_for_organization(access_token, org_name)
            # Displaying repositories names if found, otherwise printing a message
            if repos:
                for repo_name in repos:
                    print(repo_name)
            else:
                print(f"No repositories found for organization '{org_name}'.")
    else:
        print("No organizations found.")
