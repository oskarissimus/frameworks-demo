import requests

# List of GitHub repositories to fetch stats for
repositories = ["angular/angular", "facebook/react", "vuejs/core", "sveltejs/svelte"]


# Function to get the total number of pages from the 'Link' header
def get_total_pages(link_header):
    if link_header is None:
        return 1
    parts = link_header.split(",")
    last_page_link = [part for part in parts if 'rel="last"' in part]
    if not last_page_link:
        return 1
    last_page_url = last_page_link[0].split(";")[0].strip("<> ")
    page_param = last_page_url.split("page=")[-1]
    return int(page_param)


# Function to fetch repository statistics
def fetch_repo_stats(repo):
    base_url = f"https://api.github.com/repos/{repo}"
    response = requests.get(base_url)

    if response.status_code != 200:
        return f"Error fetching data for {repo}: {response.status_code}"

    data = response.json()

    # General repository stats
    stats = {
        "name": repo,
        "watchers_count": data.get("subscribers_count", "N/A"),
        "forks_count": data.get("forks_count", "N/A"),
        "stars_count": data.get("stargazers_count", "N/A"),
    }

    # Fetching additional details
    issues_response = requests.get(f"{base_url}/issues?state=all&per_page=1")
    prs_response = requests.get(f"{base_url}/pulls?state=all&per_page=1")
    releases_response = requests.get(f"{base_url}/releases")

    if (
        issues_response.status_code != 200
        or prs_response.status_code != 200
        or releases_response.status_code != 200
    ):
        return f"Error fetching additional data for {repo}: Issues({issues_response.status_code}), PRs({prs_response.status_code}), Releases({releases_response.status_code})"

    # Determine total number of pages for issues and PRs
    total_issues_pages = get_total_pages(issues_response.headers.get("Link"))
    total_prs_pages = get_total_pages(prs_response.headers.get("Link"))

    # Calculate total number of issues and PRs (assuming 30 items per page)
    total_issues = total_issues_pages * 30
    total_prs = total_prs_pages * 30

    # Adding additional details to stats
    stats.update(
        {
            "open_issues_count": data.get("open_issues_count", "N/A"),
            "total_issues_count": total_issues,
            "open_prs_count": len(
                [pr for pr in prs_response.json() if pr["state"] == "open"]
            ),
            "total_prs_count": total_prs,
            "releases_count": len(releases_response.json()),
            "date_of_last_release": releases_response.json()[0]["published_at"]
            if releases_response.json()
            else "N/A",
        }
    )

    return stats


# Main execution
if __name__ == "__main__":
    for repo in repositories:
        stats = fetch_repo_stats(repo)
        if isinstance(stats, dict):
            print(f"Stats for {repo}:")
            for key, value in stats.items():
                print(f"{key}: {value}")
            print()
        else:
            print(stats)
            print()
