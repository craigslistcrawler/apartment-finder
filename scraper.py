from craigslist import CraigslistForSale
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean
from sqlalchemy.orm import sessionmaker
from util import post_listing_to_slack
from slackclient import SlackClient
import time
import settings

engine = create_engine('sqlite:///listings.db', echo=False)

Base = declarative_base()

class Listing(Base):
    """
    A table to store data on craigslist listings.
    """

    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True)
    link = Column(String, unique=True)
    name = Column(String)
    price = Column(Float)
    cl_id = Column(Integer, unique=True)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

def scrape_area():
    """
    Scrapes craigslist for a certain geographic area, and finds the latest listings.
    :param area:
    :return: A list of results.
    """
    cl_p = CraigslistForSale(site=settings.CRAIGSLIST_SITE, category='mpa',
                             filters={'max_price': settings.MAX_PRICE})
    cl_s = CraigslistForSale(site=settings.CRAIGSLIST_SITE, category='sna',
                             filters={'max_price': settings.MAX_PRICE})
    cl_c = CraigslistForSale(site=settings.CRAIGSLIST_SITE, category='mca',
                             filters={'max_price': settings.MAX_PRICE})

    results = []
    gen = cl_p.get_results(sort_by='newest', limit=10)
    while True:
        print("first")
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass

            # Create the listing object.
            listing = Listing(
                link=result["url"],
                name=result["name"],
                price=price,
                cl_id=result["id"]
            )

            # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()
            results.append(result)
    gen = cl_s.get_results(sort_by='newest', limit=10)
    while True:
        print("second")
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()
                # Don't store the listing if it already exists.
        if listing is None:
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass
                    # Create the listing object.
            listing = Listing(
                link=result["url"],
                name=result["name"],
                price=price,
                cl_id=result["id"]
            )
                    # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()
            results.append(result)
    gen = cl_c.get_results(sort_by='newest', limit=10)
    while True:
        print("third")
        try:
            result = next(gen)
        except StopIteration:
            break
        except Exception:
            continue
        listing = session.query(Listing).filter_by(cl_id=result["id"]).first()

        # Don't store the listing if it already exists.
        if listing is None:
            price = 0
            try:
                price = float(result["price"].replace("$", ""))
            except Exception:
                pass
            # Create the listing object.
            listing = Listing(
                link=result["url"],
                name=result["name"],
                price=price,
                cl_id=result["id"]
            )
                    # Save the listing so we don't grab it again.
            session.add(listing)
            session.commit()
            results.append(result)

    return results

def do_scrape():
    """
    Runs the craigslist scraper, and posts data to slack.
    """
    # Create a slack client.
    sc = SlackClient(settings.SLACK_TOKEN)

    # Get all the results from craigslist.
    all_results = []
    print("starting")
    all_results += scrape_area()

    print("{}: Got {} results".format(time.ctime(), len(all_results)))

    # Post each result to slack.
    for result in all_results:
        post_listing_to_slack(sc, result)
