import pandas as pd
import markdown
import math

CATEGORY_MAPPING = {
    "C++": "C",
    "C#": "C",
    "Cuda": "C",
    "Xtend": "Java",
    "SCSS": "CSS",
    "Handlebars": "HTML",
    "ShaderLab": "Shader",
    "Blade": "PHP",
    "Jupyter": "Python",
    "Objective-C": "C",
    "AutoIt": "Other",
    "Nix": "Other",
    "Markdown": "Other",
    "HCL": "Other",
    "R": "Other",
    "Clojure": "Other",
}

def load_projects(csv_file):
    # Load CSV
    df = pd.read_csv(csv_file)
    
    # Normalize categories
    df['category'] = df['category'].replace(CATEGORY_MAPPING)
    
    return df

def generate_markdown(df, output_file):
    total_projects = len(df)
    rounded_total = round(total_projects, -2)  # Round to the nearest hundred
    
    # Group by category and sort by category size, excluding 'Other'
    category_counts = df['category'].value_counts()
    sorted_categories = [cat for cat in category_counts.index if cat != "Other"]
    sorted_categories.append("Other")  # Place 'Other' at the end
    
    markdown_content = "# Awesome African Open-Source Projects\n\n"
    markdown_content += f"A curated list of {rounded_total}+ awesome open-source projects made by African developers.\n\n"
    markdown_content += "If you would like to contribute, please check out our [Contribution Guide](docs/CONTRIBUTING.md).\n\n"
    markdown_content += "## Contents\n"
    for category in sorted_categories:
        markdown_content += f"- [{category}](#{category.lower().replace(' ', '-')})\n"
    markdown_content += "\n"
    
    for category in sorted_categories:
        markdown_content += f"### {category}\n\n"
        group = df[df['category'] == category]
        sorted_group = group.sort_values(by=['stars'], ascending=False)
        for _, row in sorted_group.iterrows():
            markdown_content += f"- [{row['name']}]({row['url']}) – {row['description']}\n"
        markdown_content += "\n"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return markdown_content

if __name__ == "__main__":
    csv_file = r"data/finalists-data.csv"  # Input file
    output_file = "/README.md"  # Markdown Output file
    
    df = load_projects(csv_file)
    generate_markdown(df, output_file)
    
    print(f"Markdown file generated: {output_file}")
