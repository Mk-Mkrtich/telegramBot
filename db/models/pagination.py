class Paginator:
    def __init__(self, db_cursor, table_name, page_size=5):
        self.cur = db_cursor
        self.table_name = table_name
        self.page_size = page_size
        self.current_page = 0
        self.total_pages = 0
        self.offset = 0

    def update_total_pages(self, total_records):
        self.total_pages = (total_records + self.page_size - 1) // self.page_size

    def get_page(self, page):
        self.current_page = page
        self.offset = self.current_page * self.page_size

    def next_page(self):
        if self.current_page < self.total_pages - 1:
            self.current_page += 1
        self.get_page(self.current_page)
        return self.current_page

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
        self.get_page(self.current_page)
        return self.current_page

    def first_page(self):
        self.current_page = 0
        self.get_page(self.current_page)
        return self.current_page

    def last_page(self):
        self.current_page = self.total_pages - 1
        self.get_page(self.current_page)
        return self.current_page
