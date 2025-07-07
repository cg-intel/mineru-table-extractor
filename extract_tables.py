import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
import re
import json
import sys

def run_mineru_and_extract(pdf_path_str):
    pdf_path = Path(pdf_path_str)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Unable to find PDF file: {pdf_path}")

    product_name = pdf_path.stem.split("_Spec")[0]
    output_dir = pdf_path.with_name(f"{product_name}")
    md_file = output_dir / output_dir.name / "auto" / f"{pdf_path.stem}.md"
    final_output = pdf_path.with_name(f"{product_name}_tables.md")

    print(f"MinerU extracting: {pdf_path.name}")
    subprocess.run(["mineru", "-p", str(pdf_path), "-o", str(output_dir)], check=True)

    if not md_file.exists():
        raise FileNotFoundError(f"Unable to find MinerU extracted md file: {md_file}")

    with open(md_file, encoding="utf-8") as f:
        content = f.read()

    config_path = Path("spec_table_config.json")
    if config_path.exists():
        with open(config_path, "r", encoding="utf-8") as cf:
            config = json.load(cf)
            valid_titles = config.get("valid_titles", [])
    else:
        # default tables
        valid_titles = ["规格参数", "订购指南", "选配件", "规格", "订购信息"]

    pattern = re.compile(r"(?:^|\n)([#]*\s*(" + "|".join(valid_titles) + r")\s*[:：]?)\s*<html>", re.IGNORECASE)
    matches = list(pattern.finditer(content))

    def table_to_markdown(table_html: str, section_title: str) -> str:
        md_lines = [f"## {section_title}"]
        soup = BeautifulSoup(table_html, "html.parser")
        rows = soup.find_all("tr")
        current_subsection = ""
        for row in rows:
            cells = row.find_all(["td", "th"])
            texts = [cell.get_text(strip=True) for cell in cells]
            if len(texts) == 3:
                main_cat, sub_cat, val = texts
                if main_cat:
                    md_lines.append(f"\n### {main_cat}")
                    current_subsection = sub_cat
                if sub_cat:
                    md_lines.append(f"\n#### {sub_cat}")
                else:
                    md_lines.append(f"\n#### {current_subsection}")
                md_lines.append(val)
            elif len(texts) == 2:
                sub_cat, val = texts
                if sub_cat:
                    md_lines.append(f"\n#### {sub_cat}")
                md_lines.append(val)
            elif len(texts) == 1:
                md_lines.append(texts[0])
        return "\n".join(md_lines)

    markdown_blocks = []
    for match in matches:
        title = match.group(2).strip()
        html_start = match.end()
        sub_soup = BeautifulSoup(content[html_start:], "html.parser")
        table = sub_soup.find("table")
        if table:
            markdown_blocks.append(table_to_markdown(str(table), section_title=title))

    if markdown_blocks:
        with open(final_output, "w", encoding="utf-8") as f:
            f.write(f"# {product_name}\n\n")
            f.write("\n\n".join(markdown_blocks))
        print(f"Parse table complete: {final_output}")
    else:
        print("Unable to find table")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python extract_spec_tables.py <PDF file path>")
    else:
        run_mineru_and_extract(sys.argv[1])