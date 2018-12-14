import url_helpers as convert
import unittest

class EnrichItemsDescPlTest(unittest.TestCase):

    legacy_url = "http://allegro.pl/listing/user/listing.php?string=zaproszenia%2Cwinietki%20i%20zawieszki%20%C5%9Blubne&us_id=4411135&id=74177&order=m&bmatch=base-relevance-floki-5-nga-odz-1-2-0222"

    regular_url_with_alias = "https://allegro.pl/drukarki-i-skanery-4578?string=proszek%20do%20tonera%20drukarki%20laserowej%20hp&order=p&bmatch=base-relevance-floki-5-nga-ele-1-3-0403"

    regular_url = "https://allegro.pl/listing?string=proszek&order=p&bmatch=base-relevance-floki-5-nga-fash-1-3-0403"

    def test_if_extraction_works_for_legacy_urls(self):
        # when
        category, phrase, department = convert.clean_url(self.legacy_url)

        #then
        self.assertEqual(category, "0")
        self.assertEqual(phrase, "zaproszenia,winietki i zawieszki ślubne")
        self.assertEqual(department, "odz")


    def test_if_extraction_works_for_aliases(self):
        # when
        category, phrase, department = convert.clean_url(self.regular_url_with_alias)

        # then
        self.assertEqual(category, "drukarki-i-skanery-4578")
        self.assertEqual(phrase, "proszek do tonera drukarki laserowej hp")
        self.assertEqual(department, "ele")


    def test_if_extraction_works_regular_url(self):
        # when
        category, phrase, department = convert.clean_url(self.regular_url)

        # then
        self.assertEqual(category, "0")
        self.assertEqual(phrase, "proszek")
        self.assertEqual(department, "fash")


    string_as_second_url_param = "https://allegro.pl/czesci-samochodowe-620?order=m&string=lusterka.samochodowe%20boczne%20vw%20golf%20VI&bmatch=base-relevance-floki-5-nga-aut-1-3-0222"

    def test_if_order_of_params_can_be_different(self):
        #when
        category, phrase, department = convert.clean_url(self.string_as_second_url_param)

        #then
        self.assertEqual(category, "czesci-samochodowe-620")
        self.assertEqual(phrase, "lusterka.samochodowe boczne vw golf VI")
        self.assertEqual(department, "aut")


    def test_if_category_alias_resolution_works(self):
        # given
        category_alias, phrase, department = convert.clean_url(self.regular_url_with_alias)

        # when
        categoryId = convert.resolve_category_alias(category_alias)

        #then
        self.assertEqual(categoryId, "4578")
        self.assertEqual(phrase, "proszek do tonera drukarki laserowej hp")
        self.assertEqual(department, "ele")


if __name__ == '__main__':
    unittest.main()