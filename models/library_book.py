from odoo import models, fields, api
from datetime import timedelta

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'library.book'
    _order = 'release_date desc, name'
    _rec_name = 'short_name'

    name = fields.Char('Title', required=True)
    short_name = fields.Char('Short Title', required=True)
    notes = fields.Text('Internal Notes')
    desc = fields.Html('Description', sanitize=True, strip_style=False)
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    release_date = fields.Date('Release Date')
    date_updated = fields.Datetime('Last updated')
    state = fields.Selection([
        ('draft', 'Not Available'),
        ('available', 'Available'),
        ('lost', 'Lost')],
        'State')
    page = fields.Integer('Number of Pages', 
                          groups='base.group_user', 
                          states={'lost': [('readonly', True)]},
                          help='Total book page count', company_dependent=False)
    reader_rating = fields.Float(
        'Reader Average Rating',
        digits=(14, 4))
    author_ids = fields.Many2many(
        'res.partner', 
        string='Authors')
    cost_price = fields.Float(
        'Book Cost', digits='Book Price' )
    currency_id = fields.Many2one(
        'res.currency', string="Currency")
    retail_price = fields.Monetary(
        'Retail Price',
        # optional: currency_field='currency_id',)
    )
    publisher_id = fields.Many2one(
        'res.partner', string='Publisher',
        # optional:
        # ondelete='set null',
        # context={},
        # domain=[],
        )
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=True
    )


    @api.depends('release_date')
    def _compute_age(self):
        today = fields.Date.today()
        for book in self:
            if book.release_date:
                delta = today - book.release_date
                book.age_days = delta.days
            else:
                book.age_days = 0

    def _inverse_age(self):
        today = fields.Date.today()
        for book in self.filtered('release_date'):
            d = today - timedelta(days=book.age_days)
            book.release_date = d


    def _search_age(self, operator, value):
        today = fields.Date.today()
        value_days = timedelta(days=value)
        value_date = today - value_days
        # convert the operator:
        # book with age > value have a date < value_date
        operator_map = {
            '>': '<', '>=': '<=',            
            '<': '>', '<=': '>=',
        }
        new_op = operator_map.get(operator, operator)
        return [('release_date', new_op, value_date)]
    
    # Constraints with database-level constraints
    # _sql_constraints = [
    #     ('name_uniq', 'UNIQUE (name)',
    #      'Book title must be unique.'),
    #      ('positive_page', 'CHECK(pages>0)',
    #       'No of pages must be positive')
    # ]

    # Constraints with odoo server-level constraints
    # @api.constrains('date_release')
    # def _check_release_date(self):
    #     for record in self:
    #         if record.date_release and record.date_release > fields.Date.today():
    #             raise models.ValidationError('Release date must be in the past')




class ResPartner(models.Model):
    _inherit = 'res.partner'

    published_book_ids = fields.One2many(
        'library.book', 'publisher_id', 
        string='Published Book')
    authored_book_ids = fields.Many2many(
        'library.book',
        string='Authored Books',
        # relation='library_book_res_partner_rel'  # optional
    )

