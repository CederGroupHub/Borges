# Steps to scrape ECS websites:

`$J = an ECS journal`, one of EEL, JES, JSS, SSL.

1. Run script `python issue_link.py -j $J`, the issue links for a journal will be saved in a `$J_issue_link.jl`
2. Run script `python Borges/db_scripts/insert_jl.py -i $J_issue_link.jl -c $J_issue`
3. Run script `python abstract_link.py -j $J` to record all paper links.
4. Run script `python build_paper_col.py -j $J` to build the paper collection.
5. Run script `python metadata.py -j $J` to scrape paper metadata.
6. After getting agreement from the ECS publisher, run script `python paper_html.py -j $J` to download the paper
HTML string.