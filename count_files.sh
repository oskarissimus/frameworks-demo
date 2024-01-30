#!/bin/bash

# List of your project directories and their important files
declare -A projects
projects=(["counter-next"]="counter-next/app/page.tsx" 
          ["counter-angular"]="counter-angular/src/app/app.component.ts counter-angular/src/app/app.component.html" 
          ["counter-vue"]="counter-vue/src/App.vue" 
          ["counter-svelte"]="counter-svelte/src/App.svelte")


# Loop through each project
for project in "${!projects[@]}"; do
    echo "Project: $project"
    
    # Count total files
    total_files=$(find "$project" -type f | wc -l)
    echo "Total files: $total_files"
    
    # Count git versioned files
    git_files=$(git -C "$project" ls-files | wc -l)
    echo "Git versioned files: $git_files"

    # Count files in node_modules
    if [ -d "$project/node_modules" ]; then
        node_modules_files=$(find "$project/node_modules" -type f | wc -l)
    else
        node_modules_files=0
    fi
    echo "Files in node_modules: $node_modules_files"

    # Count SLOC in important files
    important_files=${projects[$project]}
    sloc=$(cloc $important_files --sum-one --quiet | grep 'SUM' | awk '{print $5}')
    echo "SLOC in important files: $sloc"

    # Count npm packages
    if [ -f "$project/package.json" ]; then
        npm_packages=$(cat "$project/package.json" | grep '"dependencies": {' -A 100 | grep -v '}' | wc -l)
        dev_npm_packages=$(cat "$project/package.json" | grep '"devDependencies": {' -A 100 | grep -v '}' | wc -l)
        let npm_packages+=dev_npm_packages
    else
        npm_packages=0
    fi
    echo "NPM packages installed: $npm_packages"

    # Check and count npm packages
    if [ -f "$project/package-lock.json" ]; then
        npm_packages=$(grep '"version"' "$project/package-lock.json" | wc -l)
    elif [ -f "$project/yarn.lock" ]; then
        npm_packages=$(grep '^[^ \t]' "$project/yarn.lock" | wc -l)
    else
        npm_packages=0
    fi
    echo "NPM packages installed (including transitive dependencies): $npm_packages"
    echo
done