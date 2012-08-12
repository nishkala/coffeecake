from django.db import models

class Country(models.Model):
	name = models.CharField(max_length=20)
	
	class Meta:
		verbose_name_plural = 'countries'
		app_label = 'coffeecake'
	
	def __unicode__(self):
		return unicode(self.name)
	
class Bank(models.Model):
	name = models.CharField(max_length=20)
	country = models.ForeignKey(Country)
	
	class Meta:
		app_label = 'coffeecake'
		
	def __unicode__(self):
		return unicode(self.name)

class Account(models.Model):
	ACCOUNT_TYPES = (
		('C', 'Chequing'),
		('S', 'Saving'),
		('X', 'Credit Card'),
		('I', 'Investment'),
		('L', 'Loan'),
		('R', 'Retirement')
	)
	name = models.CharField(max_length=50)
	type = models.CharField(max_length=1, choices=ACCOUNT_TYPES)
	currency = models.CharField(max_length=3)
	active = models.BooleanField()
	bank = models.ForeignKey(Bank)
	
	class Meta:
		app_label = 'coffeecake'
	
	def __unicode__(self):
		return unicode(self.name)
	
class LogicalAccount(models.Model):
	ACCOUNT_TYPES = (
		('L', 'Long-Term Savings'),
		('T', 'Midterm Savings'),
		('N', 'Rolling saving'),
		('M', 'Monthly')
	)
	name = models.CharField(max_length=50)
	type = models.CharField(max_length=1, choices=ACCOUNT_TYPES)
	active = models.BooleanField()
	
	class Meta:
		app_label = 'coffeecake'
	
	def __unicode__(self):
		return unicode(self.name)
		
class Tag(models.Model):
	name = models.CharField(max_length=50)
	
	class Meta:
		app_label = 'coffeecake'
	
	def __unicode__(self):
		return unicode(self.name)
	
class LogicalTransaction(models.Model):
	TRANSACTION_TYPE = (
		('W', 'Withdrawal'),
		('D', 'Deposit'),
		('T', 'Transfer')
	)
	transaction_date = models.DateField()
	amount = models.DecimalField(max_digits=20, decimal_places=2)
	type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
	currency = models.CharField(max_length=3)
	description = models.CharField(max_length=256)
	payee = models.CharField(max_length=256)
	account = models.ForeignKey(LogicalAccount)
	linked_transaction = models.ForeignKey('self', null=True, blank=True)
	tag = models.ManyToManyField(Tag, blank=True, null=True)
	
	class Meta:
		app_label = 'coffeecake'
	
	def __unicode__(self):
		return unicode(str(self.transaction_date) + " " + str(self.amount) + self.description + self.payee)
	
class Transaction(models.Model):
	TRANSACTION_TYPE = (
		('W', 'Withdrawal'),
		('D', 'Deposit'),
		('T', 'Transfer')
	)
	transaction_date = models.DateField()
	amount = models.DecimalField(max_digits=20, decimal_places=2)
	type = models.CharField(max_length=20, choices=TRANSACTION_TYPE)
	currency = models.CharField(max_length=3, blank=True)
	description = models.CharField(max_length=256, blank=True)
	payee = models.CharField(max_length=256, blank=True)
	account = models.ForeignKey(Account)
	linked_transaction = models.ForeignKey('self', null=True, blank=True)
	logical = models.ManyToManyField(LogicalTransaction)
	
	class Meta:
		app_label = 'coffeecake'
	
	def __unicode__(self):
		return unicode(str(self.transaction_date) + " " + str(self.amount))
		
class Stock(models.Model):
	symbol = models.CharField(max_length=5)
	
	class Meta:
		app_label = 'coffeecake'
	
	def __unicode__(self):
		return unicode(self.symbol)
		
class StockTransaction(Transaction):
	trade_price = models.DecimalField(max_digits=20, decimal_places=2)
	stock = models.ForeignKey(Stock)
	num_shares = models.DecimalField(max_digits=20, decimal_places=3)

	class Meta:
		app_label = 'coffeecake'
	
	def __unicode(self):
		return unicode(self.stock) + unicode(self.trade_price) + unicode(self.num_shares)