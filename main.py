import arxiv,json,os,logging
def setup_logging():
    logging.basicConfig(
        filename='arxiv_downloader.log',
        level=logging.DEBUG,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        encoding='utf-8',
        filemode='w' 
    )
    logging.info("Logging setup complete.")
def init():
    return arxiv.Client()
def clear_pdf_directory():
    pdf_dir = "./pdf"
    for filename in os.listdir(pdf_dir):
        file_path = os.path.join(pdf_dir, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
    logging.info("PDF directory cleared.")
def search(client,keyword, max_results):
    search = arxiv.Search(
        query=keyword,
        max_results=max_results,sort_by = arxiv.SortCriterion.SubmittedDate
    )
    return client.results(search)
def get_keywords():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cfg', 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    keywords = config.get('keywords', [])
    return ' '.join(keywords)
def get_max_results():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cfg', 'config.json')
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config.get('maxResults')
def download_pdfs(results):
    for result in results:
        pdf = result.download_pdf(dirpath="./pdf", filename=result.title.replace(" ", "_") + ".pdf")
def main():
    client = init()
    keyword = get_keywords()
    max_results = get_max_results()
    results = search(client,keyword, max_results)
    download_pdfs(results)
if __name__ == "__main__":
    clear_pdf_directory()
    setup_logging()
    main()