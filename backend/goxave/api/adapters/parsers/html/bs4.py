from functools import reduce

from bs4 import BeautifulSoup, Tag


class HTMLParser(BeautifulSoup):
    def __init__(self, html_content: str):
        super().__init__(html_content, "html5lib")

    def nested_find_all(
        self,
        elements: list[Tag],
        params: list[tuple[str | list | None, str | None, str | None]],
    ) -> list[Tag]:
        def find_nested(
            el_list: list[Tag],
            param: tuple[str | list | None, str | None, str | None],
        ) -> list[Tag]:
            attr_value, attr_name = param[0], param[1]
            tag_name = param[2] if len(param) == 3 else None

            nested = []
            for el in el_list:
                kwargs = {attr_name: attr_value} if attr_name and attr_value else {}
                found = (
                    el.find_all(name=tag_name, attrs={**kwargs})
                    if tag_name
                    else el.find_all(attrs={**kwargs})
                )
                nested.extend(found)
            return nested

        return reduce(find_nested, params, elements)

    def get_item_given_index(
        self, items: list[Tag], index
    ) -> Tag | None:  # -> Any | None:
        if isinstance(items, list) and len(items) > index:
            return items[index]
        return None
