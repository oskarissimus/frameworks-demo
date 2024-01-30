from github import Github
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Initialize a Github instance:
# If you have a GitHub access token, you can provide it here to avoid rate limiting
# g = Github("your_access_token")
g = Github()

repositories = ["angular/angular", "facebook/react", "vuejs/core", "sveltejs/svelte"]


def fetch_repo_stats(repo_name):
    repo = g.get_repo(repo_name)

    stats = {
        "name": repo.full_name,
        "watchers_count": repo.subscribers_count,
        "forks_count": repo.forks_count,
        "stars_count": repo.stargazers_count,
        "open_issues_count": repo.open_issues_count,
        "total_issues_count": repo.get_issues(state="all").totalCount,
        "open_prs_count": repo.get_pulls(state="open").totalCount,
        "total_prs_count": repo.get_pulls(state="all").totalCount,
    }

    releases = repo.get_releases()
    if releases.totalCount > 0:
        latest_release = releases[0]
        stats["releases_count"] = releases.totalCount
        stats["date_of_last_release"] = latest_release.published_at
    else:
        stats["releases_count"] = 0
        stats["date_of_last_release"] = "N/A"

    return stats


def color_formatter(val, min_val, max_val):
    if val == min_val:
        color = "red"
    elif val == max_val:
        color = "green"
    else:
        color = "yellow"
    return f"background-color: {color}"


def apply_color_formatting(df):
    styled_df = df.copy()
    for column in styled_df.columns:
        if styled_df[column].dtype in [int, float]:
            max_val = styled_df[column].max()
            min_val = styled_df[column].min()
            styled_df[column] = styled_df[column].apply(
                lambda x: color_formatter(x, min_val, max_val)
            )
    return styled_df


if __name__ == "__main__":
    stats_list = [fetch_repo_stats(repo_name) for repo_name in repositories]
    df = pd.DataFrame(stats_list)
    styled_df = apply_color_formatting(df)
    print(styled_df)

    # Optionally save the styled DataFrame as an image
    sns.set()
    fig, ax = plt.subplots(figsize=(10, 5))  # Adjust size as needed
    ax.axis("tight")
    ax.axis("off")
    ax.table(
        cellText=styled_df.values,
        colLabels=styled_df.columns,
        cellLoc="center",
        loc="center",
        cellColours=styled_df.to_numpy(),
    )
    plt.savefig("repo_stats_table.png")
