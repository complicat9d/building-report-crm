from typing import List, Tuple


def paginate(objects: List, page: int, per_page: int) -> Tuple:
    total_items = len(objects)
    total_pages = (total_items // per_page) + (1 if total_items % per_page > 0 else 0)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_objects = objects[start:end]

    return total_pages, paginated_objects
