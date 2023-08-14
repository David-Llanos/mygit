for branch in $(git branch -r); do
    branch_name=$(echo "$branch" | sed 's/origin\///')
    if [[ "$branch_name" != *"->"* ]]; then
        for commit in $(git rev-list --reverse "$branch_name"); do
            username=$(git log -1 --format='%an' "$commit")
            commit_date=$(git log -1 --format='%ad' --date=format:'%Y-%m-%d %H:%M:%S' "$commit")
            git ls-tree -r "$commit" --name-only | while IFS= read -r filename; do
                size=$(git cat-file -s "$commit:$filename")
                echo "\"$branch_name\",\"$commit\",\"$username\",\"$commit_date\",\"$size\",\"$filename\"" >> file_list.csv
            done
        done
    fi
done
