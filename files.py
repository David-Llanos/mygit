import git
import os

# Path to the Git repository
repo_path = "/path/to/your/repository"

# Open the Git repository
repo = git.Repo(repo_path)

# Create a CSV header
csv_lines = ["Branch,Commit,Username,Date,Size,Filename"]

# Loop through branches
for branch in repo.remote().refs:
    if branch.remote_head:  # Exclude HEAD
        branch_name = branch.remote_head.name
        csv_lines.append(f"\"{branch_name}\",,,,\"\",\"\"")  # Header for the branch
        for commit in repo.iter_commits(branch_name):
            commit_hash = commit.hexsha
            author_name = commit.author.name
            commit_date = commit.authored_datetime.strftime('%Y-%m-%d %H:%M:%S')
            for item in commit.tree.traverse():
                if item.type == "blob":
                    filename = item.path
                    size = item.size
                    csv_lines.append(f"\"\",\"{commit_hash}\",\"{author_name}\",\"{commit_date}\",\"{size}\",\"{filename}\"")

# Write to CSV file
with open("file_list.csv", "w") as csv_file:
    csv_file.write("\n".join(csv_lines))
