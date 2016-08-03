from google.appengine.ext import ndb
import jinja2
import os
import webapp2
from google.appengine.api import users

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))
class Customer(ndb.Model):
    name = ndb.StringProperty(required=True)
    address = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
class order(ndb.Model):
    customer_key = ndb.KeyProperty(kind='Customer')
    crust = ndb.StringProperty(required=True)
    size = ndb.StringProperty(required=True)
    sauce = ndb.StringProperty(required=True)
    vegan = ndb.StringProperty(required=True)
    cheese = ndb.StringProperty(required=True)
    toppings = ndb.StringProperty(required=True)


class MainHandler(webapp2.RequestHandler):

    def get(self):
        user = users.get_current_user()
        user_info = {
        'nickname_answer': self.request.get('nickname'),
        'log_out': self.request.get('log_out_url')
        }
        if user:
            greeting = ('Welcome, %s! (<a href="%s">sign out</a>)' %
                        (user.nickname(), users.create_logout_url('/')))
        else:
            greeting = ('<a href="%s">Sign in or register</a>.' %
                        users.create_login_url('/'))
        self.response.out.write('%s' % greeting)
        template = jinja_environment.get_template('templates/input_order.html')
        template2 = jinja_environment.get_template('templates/customer_order.html')
        self.response.write(template.render())

    def post(self):
        template = jinja_environment.get_template('templates/output_order.html')
        name_value = self.request.get('name')
        crust_value = self.request.get('crust')
        size_value = self.request.get('size')
        sauce_value = self.request.get('sauce')
        vegan_value = self.request.get('vegan')
        cheese_value = self.request.get('cheese')
        toppings_value = self.request.get('toppings')
        address_value = self.request.get('address')
        phone_value = self.request.get('phone')
        pizza_order = {
          'crust_answer': self.request.get('crust'),
          'size_answer': self.request.get('size'),
          'sauce_answer': self.request.get('sauce'),
          'vegan_answer': self.request.get('vegan'),
          'cheese_answer': self.request.get('cheese'),
          'toppings_answer': self.request.get('toppings'),
          }
        customer_order = {
          'address_answer': self.request.get('address'),
          'name_answer':self.request.get('name'),
          'phone_answer':self.request.get('phone')

        }
        new_order = {
          'crust_answer': self.request.get('crust'),
          'size_answer': self.request.get('size'),
          'sauce_answer': self.request.get('sauce'),
          'vegan_answer': self.request.get('vegan'),
          'cheese_answer': self.request.get('cheese'),
          'toppings_answer': self.request.get('toppings'),
          'address_answer': self.request.get('address'),
          'name_answer':self.request.get('name'),
          'phone_answer':self.request.get('phone')
        }
        customer_record = Customer(address=address_value,name=name_value,phone=phone_value)
        custkeys = customer_record.put()
        order_record = order(customer_key=custkeys,crust=crust_value, size=size_value, sauce=sauce_value, vegan=vegan_value, cheese=cheese_value,toppings=toppings_value)
        key = order_record.put()
        pizza_order['order']= key.id()
        customer_order['Customer']=key.id()

        self.response.write(template.render(new_order))
        # self.response.write(template.render(customer_order))

app = webapp2.WSGIApplication([
  ('/', MainHandler),
], debug=True)
