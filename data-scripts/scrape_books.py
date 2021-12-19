from scraping.aozora_bunko_scraper import AozoraBunkoScraper

author_list_path = "author_list.txt"
save_dir = "data"

# load author_list
with open(author_list_path, 'r', encoding='utf-8') as f:
    author_list = f.readlines()
    author_list = [s.split() for s in author_list]

scraper = AozoraBunkoScraper(save_dir)

for author_name in author_list:
    scraper.get_theauthor_books(author_name, maximum=10000, save_n=50)

scraper.save()