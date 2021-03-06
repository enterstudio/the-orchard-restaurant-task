from flask import redirect, render_template, request

from restaurantfinder import etl
from restaurantfinder.blueprints import results as results_view
from restaurantfinder import models


@results_view.route('/', methods=['GET'])
def index():
    if etl.Extractor.has_data():
        try:
            page = int(request.args.get('page'))
        except Exception:
            page = 1

        restaurants, pager = models.Restaurant.get_page(page)

        return render_template("list.html",
                               nav="results",
                               pager=pager,
                               restaurants=restaurants)
    else:
        return redirect("/etl")


@results_view.route('top/<criteria>', methods=['GET'])
def top(criteria):
    if etl.Extractor.has_data():
        try:
            page = int(request.args.get('page'))
        except Exception:
            page = 1

        restaurants, msg, pager = models.Restaurant.find_by_criteria(criteria, page)

        return render_template("list.html",
                               nav="top",
                               pager=pager,
                               msg=msg,
                               restaurants=restaurants)
    else:
        return redirect("/etl")


@results_view.route('<restaurant_id>', methods=['GET'])
def single(restaurant_id):
    if etl.Extractor.has_data():
        restaurant = models.Restaurant.get_by_id(restaurant_id)
        return render_template("single.html",
                           nav="results",
                           restaurant=restaurant)
    else:
        return redirect("/etl")