import os
import math
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskapp import app, db, bcrypt, mail
from flaskapp.forms import CreatorMsgForm, SearchForm, PersonalisedSearchForm, EventDetailForm, CustomerPreferenceForm, PersonalDetailForm, LoginForm, RegistrationForm, ResetPasswordForm, RequestResetForm, CreateEventForm
from flaskapp.models import User, Event, Tag, Wishlist, Cart, Booking, Notification, Messages
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
import stripe
stripe.api_key = app.config['STRIPE_SECRET_KEY']


@app.route("/msgtocreator/<int:eventid>", methods=['POST'])
def sendmsgtocreator(eventid):
    event = Event.query.get_or_404(eventid)
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    msg_form = CreatorMsgForm(request.form, prefix="creatormsg-form")
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    event = Event.query.filter_by(id=eventid).first()
    creator_id=event.creator_id
    if msg_form.validate_on_submit:
        content=msg_form.content_msg.data
        sender=user.id
        creator=creator_id
        msg = Messages(content=content, sender=sender, receiver=creator, sendername=user.username)
        db.session.add(msg)
        db.session.commit()
        flash('message successfully sent!', 'info')
        return redirect(url_for('event', event_id=event.id))
    flash('message failed to send', 'danger')
    return render_template('event.html', title=event.title, event=event, login_form=login_form, regis_form=regis_form, search_form=search_form, msg_form=msg_form)

@app.route("/cyclingevents", methods=['GET', 'POST'])
def cycling():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter_by(tags='cycling').order_by(Event.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('allevents.html', login_form=login_form, regis_form=regis_form, events=events, search_form=search_form)

@app.route("/swimmingevents", methods=['GET', 'POST'])
def swimming():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter_by(tags='swimming').order_by(Event.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('allevents.html', login_form=login_form, regis_form=regis_form, events=events, search_form=search_form)

@app.route("/musicevents", methods=['GET', 'POST'])
def music():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter_by(tags='music').order_by(Event.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('allevents.html', login_form=login_form, regis_form=regis_form, events=events, search_form=search_form)

@app.route("/tripevents", methods=['GET', 'POST'])
def trip():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter_by(tags='trip').order_by(Event.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('allevents.html', login_form=login_form, regis_form=regis_form, events=events, search_form=search_form)

@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    if user.id==1:
        events = Event.query.order_by(Event.date_posted.desc()).slice(0,9)
        users = User.query.order_by(User.id.desc()).slice(0,9)
        creators = User.query.filter_by(is_creator=True).order_by(User.id.desc()).slice(0,9)
        return render_template('adminmain.html', events=events, creators=creators, users=users)
    else:
        return redirect(url_for('home'))

@app.route('/admin_event/<int:eventid>', methods=['GET', 'POST'])
@login_required
def adminevent(eventid):
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    if user.id==1:
        event = Event.query.filter_by(id=eventid).first()
        return render_template('adminevent.html', event=event)
    else:
        return redirect(url_for('home'))

@app.route('/stripeaccountcomplete')
@login_required
def stripe_account_complete():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    if user.stripe_acc_id:
        user.is_stripe_complete=True
        db.session.commit()
        return redirect(url_for('dashboard'))
    else:
        return 'error'

@app.route('/create-express-account', methods=['GET', 'POST'])
@login_required
def create_express_account():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    account = stripe.Account.create(
      type='express',
      email=user.email,
      country=user.country,
    )
    account_id = account.id
    user.stripe_acc_id = account_id
    db.session.commit()
    account_links = stripe.AccountLink.create(
      account=account_id,
      refresh_url='https://testsite09.pythonanywhere.com/dashboard',
      return_url='https://testsite09.pythonanywhere.com/stripeaccountcomplete',
      type='account_onboarding',
    )
    return redirect(account_links.url, code=303)

@app.route('/create-checkout-session', methods=['POST'])
@login_required
def create_checkout_session():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    totalprice=0
    line_items = []
    for item in cart:
        eventid = item.event_id
        print(eventid)
        event = Event.query.filter_by(id=eventid).first()
        eventprice = event.price
        quantity = item.quantity
        if event.attendee1 and quantity >= event.attendee1:
            eventprice = event.discount1
        if event.attendee2 and quantity >= event.attendee2:
            eventprice = event.discount2
        if event.attendee3 and quantity >= event.attendee3:
            eventprice = event.discount3
        if event.attendee4 and quantity >= event.attendee4:
            eventprice = event.discount4
        if event.attendee5 and quantity >= event.attendee5:
            eventprice = event.discount5
        if event.attendee6 and quantity >= event.attendee6:
            eventprice = event.discount6
        if event.attendee7 and quantity >= event.attendee7:
            eventprice = event.discount7
        if event.attendee8 and quantity >= event.attendee8:
            eventprice = event.discount8
        eventtitle=event.title
        line_item = {
            'price_data': {
                'currency':'usd',
                'product_data': {
                    'name':eventtitle,
                    },
                'unit_amount':eventprice * 100,
                },
                'quantity': quantity,
            }
        line_items.append(line_item)
        eventprice = eventprice * quantity
        totalprice = totalprice+eventprice
    # for item in cart:
    #     eventid = item.event_id
    #     print(eventid)
    #     event = Event.query.filter_by(id=eventid).first()
    #     eventprice = event.price
    #     print(eventprice)
    #     quantity = item.quantity
    #     if event.attendee1 and quantity >= event.attendee1:
    #         eventprice = event.discount1
    #     if event.attendee2 and quantity >= event.attendee2:
    #         eventprice = event.discount2
    #     if event.attendee3 and quantity >= event.attendee3:
    #         eventprice = event.discount3
    #     if event.attendee4 and quantity >= event.attendee4:
    #         eventprice = event.discount4
    #     if event.attendee5 and quantity >= event.attendee5:
    #         eventprice = event.discount5
    #     if event.attendee6 and quantity >= event.attendee6:
    #         eventprice = event.discount6
    #     if event.attendee7 and quantity >= event.attendee7:
    #         eventprice = event.discount7
    #     if event.attendee8 and quantity >= event.attendee8:
    #         eventprice = event.discount8
    #     totalprice = totalprice + eventprice
    # session = stripe.checkout.Session.create(
    # payment_method_types=['card'],
    #         line_items=[{
    #             'price_data': {
    #                 'currency': 'usd',
    #                 'product_data': {
    #                     'name': 'Listeo',
    #                 },
    #                 'unit_amount': totalprice * 100,
    #             },
    #             'quantity': 1,
    #         }],
    #     mode='payment',
    #     success_url='https://testsite09.pythonanywhere.com/order/success?session_id={CHECKOUT_SESSION_ID}',
    #     cancel_url='https://testsite09.pythonanywhere.com/cart',
    # )
    # line_items = [{
    #     'price_data': {
    #         'currency':'usd',
    #         'product_data': {
    #             'name':'Listeo',
    #             },
    #         'unit_amount':totalprice * 100,
    #         },
    #         'quantity': 1,
    #     },
    #     {
    #     'price_data': {
    #         'currency':'usd',
    #         'product_data': {
    #             'name':'Another',
    #             },
    #         'unit_amount':totalprice * 100,
    #         },
    #         'quantity': 1,
    #     }]
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        payment_intent_data={
            'transfer_group':user.id,
        },
        mode='payment',
        success_url='https://testsite09.pythonanywhere.com/order/success?session_id={CHECKOUT_SESSION_ID}',
        cancel_url='https://testsite09.pythonanywhere.com/cart',
    )
    return redirect(session.url, code=303)

@app.route('/order/success', methods=['GET'])
@login_required
def order_success():
    session = stripe.checkout.Session.retrieve(request.args.get('session_id'))
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    cart = Cart.query.filter_by(user_id=user.id).all()
    application_fee_amount_percentage = 10
    if session:
        for item in cart:
            quantity = item.quantity
            eventid=item.event_id
            event=Event.query.filter_by(id=eventid).first()
            eventprice=event.price
            if event.attendee1 and quantity >= event.attendee1:
                eventprice = event.discount1
            if event.attendee2 and quantity >= event.attendee2:
                eventprice = event.discount2
            if event.attendee3 and quantity >= event.attendee3:
                eventprice = event.discount3
            if event.attendee4 and quantity >= event.attendee4:
                eventprice = event.discount4
            if event.attendee5 and quantity >= event.attendee5:
                eventprice = event.discount5
            if event.attendee6 and quantity >= event.attendee6:
                eventprice = event.discount6
            if event.attendee7 and quantity >= event.attendee7:
                eventprice = event.discount7
            if event.attendee8 and quantity >= event.attendee8:
                eventprice = event.discount8
            totalprice=eventprice*quantity
            creator_id = event.creator_id
            creator=User.query.filter_by(id=creator_id).first()
            stripe_id = creator.stripe_acc_id
            application_fee_amount = math.floor(totalprice/application_fee_amount_percentage)
            totalprice=totalprice-application_fee_amount
            transfer = stripe.Transfer.create(
              amount=totalprice*100,
              currency='usd',
              destination=stripe_id,
              transfer_group=user.id,
            )
    eventid=[]
    for item in cart:
        eventid.append(item.event_id)
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    if session:
        for item in eventid:
            user_email = current_user.email
            user = User.query.filter_by(email=user_email).first()
            booking = Booking(user_id=user.id, event_id=item)
            db.session.add(booking)
            db.session.commit()
            cartevent = Cart.query.filter_by(user_id=user.id, event_id=item).first()
            db.session.delete(cartevent)
            db.session.commit()
            event = Event.query.filter_by(id=item).first()
            str1=user.first_name
            str2=user.last_name
            fullname=" ".join([str1, str2])
            noti = Notification(user_id=event.creator_id, event=event.title, title="Event Booked", fullname=fullname)
            db.session.add(noti)
            db.session.commit()
        events_main = Event.query.order_by(Event.date_posted.desc())
        events_s1 = events_main.slice(0,3)
        events_s2 = events_main.slice(3,6)
        return render_template('eventbooksuccess.html', login_form=login_form, regis_form=regis_form, search_form=search_form, events_s1=events_s1, events_s2=events_s2)
    else:
        return redirect(url_for('home'))

@app.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
    notifications = Notification.query.filter_by(user_id=user.id).all()
    for noti in notifications:
        noti.read=True
        db.session.commit()
    return render_template('notifications.html', notifications=notifications, notifcount=notifcount, msgcount=msgcount)

@app.route('/messages', methods=['GET', 'POST'])
@login_required
def messages():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
    messages = Messages.query.filter_by(receiver=user.id).all()
    for msg in messages:
        msg.read=True
        db.session.commit()
    return render_template('messages.html', messages=messages, notifcount=notifcount, msgcount=msgcount)


@app.route("/", methods=['GET', 'POST'])
def home():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    events_main = Event.query.order_by(Event.date_posted.desc())
    events_s1 = events_main.slice(0,3)
    events_s2 = events_main.slice(3,6)
    return render_template('home.html', login_form=login_form, regis_form=regis_form, events_s1=events_s1, events_s2=events_s2, search_form=search_form)


@app.route("/cart", methods=['GET', 'POST'])
@login_required
def cart():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    cart_items = Cart.query.filter_by(user_id=user.id).all()
    idlist = []
    for item in cart_items:
        idlist.append(item.event_id)
    events = Event.query.filter(Event.id.in_((idlist))).all()

    return render_template('cart.html', login_form=login_form, regis_form=regis_form, search_form=search_form, events=events)

@app.route("/editcart/<int:eventid>/<int:quantity>", methods=['POST'])
@login_required
def editcart(eventid, quantity):
    print('accessed')
    print(eventid)
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    cart = Cart.query.filter_by(user_id=user.id, event_id=eventid).first()
    cart.quantity = quantity
    db.session.commit()
    return 'saved'

@app.route("/addtocart/<int:eventid>", methods=['POST'])
@login_required
def addtocart(eventid):
    print('accessed')
    print(eventid)
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    checkcart=Cart.query.filter_by(user_id=user.id, event_id=eventid).first()
    if checkcart:
        return 'alreadyexists'
    else:
        cart = Cart(user_id=user.id, event_id=eventid)
        db.session.add(cart)
        db.session.commit()
    return 'saved'

@app.route("/remfromcart/<int:eventid>", methods=['POST'])
@login_required
def remfromcart(eventid):
    print('accessed')
    print(eventid)
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    cart = Cart.query.filter_by(user_id=user.id, event_id=eventid).first()
    if cart:
        db.session.delete(cart)
        db.session.commit()
        return 'removed'
    else:
        return 'event not found'

@app.route("/wishlist", methods=['GET', 'POST'])
@login_required
def wishlist():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    wishlist_items = Wishlist.query.filter_by(user_id=user.id).all()
    idlist = []
    for item in wishlist_items:
        idlist.append(item.event_id)
    events = Event.query.filter(Event.id.in_((idlist))).all()

    return render_template('wishlist.html', login_form=login_form, regis_form=regis_form, search_form=search_form, events=events)


@app.route("/addwishlist/<int:eventid>", methods=['POST'])
@login_required
def addwish(eventid):
    print('accessed')
    print(eventid)
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    event = Wishlist(user_id=user.id, event_id=eventid)
    db.session.add(event)
    db.session.commit()
    return 'saved'

@app.route("/remwishlist/<int:eventid>", methods=['POST'])
@login_required
def remwish(eventid):
    print('accessed')
    print(eventid)
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    event = Wishlist.query.filter_by(user_id=user.id, event_id=eventid).first()
    if event:
        db.session.delete(event)
        db.session.commit()
        return 'removed'
    else:
        return 'event not found'

@app.route("/search", methods=['POST'])
def search():
    search_form = SearchForm(request.form, prefix="search-form")
    if search_form.validate_on_submit():
        searchword=search_form.searchword.data
        return redirect(url_for('personalised_events', keyword=searchword, location='nil', category='nil'))
    return redirect(url_for('discover'))


@app.route("/register", methods=['POST'])
def register():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    if regis_form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(regis_form.password_regis.data).decode('utf-8')
        user = User(username=regis_form.username_regis.data, email=regis_form.email_regis.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(email=regis_form.email_regis.data).first()
        login_user(user, remember=True)
        user.times_logged_in += 1
        db.session.commit()
        send_verify_account_email(user)
        flash('Your account has been created and an email has been sent to you for verification', 'info')
        return render_template('account_verification.html', search_form=search_form, regis_form=regis_form, login_form=login_form)
    return render_template('home.html', regis_form=regis_form, login_form=login_form, search_form=search_form)

@app.route("/login", methods=['POST'])
def login():
    login_form = LoginForm(request.form, prefix='login-form')
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email_login.data).first()
        user2 = User.query.filter_by(username=login_form.email_login.data).first()
        if user and bcrypt.check_password_hash(user.password, login_form.password_login.data):
            login_user(user, remember=login_form.remember.data)
            next_page = request.args.get('next')
            if user.times_logged_in == 0:
                if user.is_account_verified is False:
                    user.times_logged_in += 1
                    db.session.commit()
                    send_verify_account_email(user)
                    flash('Please check your email for account verification link', 'info')
            user.times_logged_in += 1
            db.session.commit()
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        elif user2 and bcrypt.check_password_hash(user2.password, login_form.password_login.data):
            login_user(user2, remember=login_form.remember.data)
            next_page = request.args.get('next')
            if user2.times_logged_in == 0:
                if user2.is_account_verified is False:
                    user2.times_logged_in += 1
                    db.session.commit()
                    send_verify_account_email(user2)
                    flash('Please check your email for account verification link', 'info')
            user2.times_logged_in += 1
            db.session.commit()
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
    return render_template('home.html', regis_form=regis_form, login_form=login_form, search_form=search_form)


@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if current_user.is_authenticated:
        user_email = current_user.email
        user = User.query.filter_by(email=user_email).first()
        user.is_account_verified = True
        db.session.commit()
        notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
        msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
        search_form = SearchForm(request.form, prefix="search-form")
        login_form = LoginForm(request.form, prefix="login-form")
        regis_form = RegistrationForm(request.form, prefix="register-form")
        if user.is_account_verified == False:
            return render_template('account_verification.html', search_form=search_form, regis_form=regis_form, login_form=login_form)
        if user.is_creator == True:
            events = Event.query.filter_by(event_author=user).order_by(Event.date_posted.desc())
            events = events.slice(0,9)
            total_events = events.count()
            if user.is_profile_complete == False:
                return redirect(url_for('account_details'))
            elif user.is_stripe_complete == False:
                return redirect(url_for('create_express_account'), code=307)
            return render_template('dashboard_creator.html', total_events=total_events, events=events, notifcount=notifcount, msgcount=msgcount)
        else:
            if user.is_profile_complete == False:
                return redirect(url_for('account_details'))
            return render_template('dashboard_user.html', notifcount=notifcount, msgcount=msgcount)

    else:
        return redirect(url_for('home'))

@app.route("/bookings")
@login_required
def bookings():
    notifcount = Notification.query.filter_by(user_id=current_user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=current_user.id, read=False).count()
    return render_template('dashboard_user.html', notifcount=notifcount, msgcount=msgcount)

@app.route("/initcreator")
@login_required
def become_creator():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    search_form = SearchForm(request.form, prefix="search-form")
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    if user.is_account_verified == False:
        return render_template('account_verification.html', search_form=search_form, regis_form=regis_form, login_form=login_form)
    user.is_creator = True
    db.session.commit()
    flash('You are now a creator!', 'success')
    return redirect(url_for('account_details'))

@app.route("/accountdetails")
@login_required
def account_details():
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    search_form = SearchForm(request.form, prefix="search-form")
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    if user.is_account_verified == False:
        return render_template('account_verification.html', search_form=search_form, regis_form=regis_form, login_form=login_form)
    if user.personal_details_complete == False:
        return redirect(url_for('personal_details'))
    if user.is_creator == True:
        if user.event_details_complete == False:
            return redirect(url_for('event_details'))
        elif user.preferences_complete == False:
            return redirect(url_for('preference_details'))
        else:
            user.is_profile_complete = True
            db.session.commit()
            return redirect(url_for('dashboard'))
    else:
        if user.preferences_complete == False:
            return redirect(url_for('preference_details'))
        else:
            user.is_profile_complete = True
            db.session.commit()
            return redirect(url_for('dashboard'))


@app.route("/accountdetails/personal_details", methods=['GET', 'POST'])
@login_required
def personal_details():
    form = PersonalDetailForm()
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
    if user.personal_details_complete == False:
        if form.validate_on_submit():
            user.first_name = form.first_name.data
            user.last_name = form.last_name.data
            user.contact_number = form.contact_number.data
            user.address = form.address.data
            user.city = form.city.data
            user.loc_state = form.loc_state.data
            user.zip_code = form.zip_code.data
            user.country = form.country.data
            user.personal_details_complete = True
            db.session.commit()
            return redirect(url_for('account_details'))
        return render_template('personal_details.html', form=form, notifcount=notifcount, msgcount=msgcount)
    else:
        return redirect(url_for('account_details'))

@app.route("/accountdetails/event_details", methods=['GET', 'POST'])
@login_required
def event_details():
    form = EventDetailForm()
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
    if user.event_details_complete == False:
        if form.validate_on_submit():
            if form.profile_type.data == 'company':
                user.is_profile_company = True
                user.company_details = form.company_details.data
            else:
                user.is_profile_company = False
            user.location = form.location.data
            tags = form.tags.data
            new_tag = Tag(creator_id=user.id, tag_title=tags)
            db.session.add(new_tag)
            user.event_details_complete = True
            db.session.commit()
            return redirect(url_for('account_details'))
        return render_template('event_details.html', form=form, notifcount=notifcount, msgcount=msgcount)
    else:
        return redirect(url_for('account_details'))

@app.route("/accountdetails/preference_details", methods=['GET', 'POST'])
@login_required
def preference_details():
    form = CustomerPreferenceForm()
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
    if user.preferences_complete == False:
        if form.validate_on_submit():
            user.tagp1 = form.preference_1.data
            user.tagp2 = form.preference_2.data
            user.tagp3 = form.preference_3.data
            user.preferences_complete = True
            db.session.commit()
            return redirect(url_for('account_details'))
        return render_template('preference_details.html', form=form, notifcount=notifcount, msgcount=msgcount)
    else:
        return redirect(url_for('account_details'))


@app.route("/account")
@login_required
def account():
    style = 'active'
    search_form = SearchForm(request.form, prefix="search-form")
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    if user.is_account_verified == False:
            return render_template('account_verification.html', style5=style, search_form=search_form, regis_form=regis_form, login_form=login_form)
    if user.is_profile_complete == True:
        completion=True
    else:
        completion=False
    return render_template('account.html', style4=style, completion=completion)


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/event_pics', picture_fn)

    i = Image.open(form_picture)
    i.save(picture_path)

    return picture_fn


@app.route("/create_event", methods=['GET', 'POST'])
@login_required
def create_event():
    style = 'active'
    search_form = SearchForm(request.form, prefix="search-form")
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    form = CreateEventForm()
    if form.validate_on_submit():
        user_email = current_user.email
        user = User.query.filter_by(email=user_email).first()
        title = form.title.data
        desc = form.description.data
        image1 = save_picture(form.image1.data)
        if form.image2.data:
            image2 = save_picture(form.image2.data)
        else:
            image2=''
        if form.image3.data:
            image3 = save_picture(form.image3.data)
        else:
            image3=''
        if form.image4.data:
            image4 = save_picture(form.image4.data)
        else:
            image4=''
        if form.image5.data:
            image5 = save_picture(form.image5.data)
        else:
            image5=''
        if form.image6.data:
            image6 = save_picture(form.image6.data)
        else:
            image6=''
        if form.image7.data:
            image7 = save_picture(form.image7.data)
        else:
            image7=''
        loc = form.location.data
        price = form.price.data
        date = form.date.data
        date_end = form.date_end.data
        time = form.time.data
        time_end = form.time_end.data
        days = form.days.data
        pre_know = form.pre_knowledge.data
        tags = form.tags.data
        schedule = form.schedule.data
        direction = form.direction.data
        equipment = form.equipment.data
        min_tickets = form.min_tickets.data
        offers_bool = form.offers_bool.data
        attendee1 = form.attendee1.data
        discount1 = form.discount1.data
        attendee2 = form.attendee2.data
        discount2 = form.discount2.data
        attendee3 = form.attendee3.data
        discount3 = form.discount3.data
        attendee4 = form.attendee4.data
        discount4 = form.discount4.data
        fee_cancel = form.fee_cancel.data
        prioritize = form.prioritize.data
        event = Event(event_author=user, title=title, description=desc,
                image1=image1, image2=image2, image3=image3, image4=image4,
                image5=image5, image6=image6, image7=image7, location=loc,
                price=price, date=date, days=days, pre_knowledge=pre_know,
                tags=tags, schedule=schedule, direction=direction, equipment=equipment,
                min_tickets=min_tickets, offers_bool=offers_bool, fee_cancel=fee_cancel,
                attendee1=attendee1, attendee2=attendee2, attendee3=attendee3, attendee4=attendee4,
                discount1=discount1, discount2=discount2, discount3=discount3, discount4=discount4,
                date_end=date_end, time=time, time_end=time_end, prioritize=prioritize)
        db.session.add(event)
        db.session.commit()
        event = Event.query.filter_by(creator_id=user.id).order_by(Event.date_posted.desc()).first()
        event_id = event.id
        flash('Your event has been saved!', 'success')
        return redirect(url_for('event', event_id=event_id))
    if current_user.is_creator == True:
        if current_user.is_account_verified == True:
            if current_user.is_profile_complete == True:
                print('c')
                return render_template('create_event.html', style5=style, form=form)
            else:
                flash('Complete your account details first', 'info')
                return redirect(url_for('account_details'))
        else:
            return render_template('account_verification.html', style5=style, search_form=search_form, regis_form=regis_form, login_form=login_form)
    else:
        return redirect(url_for('home'))


@app.route("/allevents", methods=['GET', 'POST'])
def allevents():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('allevents.html', login_form=login_form, regis_form=regis_form, events=events, search_form=search_form)

@app.route("/discover", methods=['GET', 'POST'])
def discover():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    form = PersonalisedSearchForm()
    print('3')
    if request.method == 'POST':
        print('1')
        if form.validate_on_submit:
            print('2')
            keyword: str = form.keyword.data
            if keyword == '':
                keyword: str = 'nil'
            location: str = form.location.data
            if location == '':
                location: str = 'nil'
            category: str = form.category.data
            if category == '':
                category: str = 'nil'
            return redirect(url_for('personalised_events', keyword=keyword, location=location, category=category))
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.date_posted.desc()).paginate(page=page, per_page=9)
    return render_template('discover.html', login_form=login_form, regis_form=regis_form, form=form, events=events, search_form=search_form)

@app.route("/personalisedevents/<string:keyword>/<string:location>/<string:category>", methods=['GET', 'POST'])
def personalised_events(keyword, location, category):
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    form = PersonalisedSearchForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            print('2')
            keyword: str = form.keyword.data
            if keyword == '':
                keyword: str = 'nil'
            location: str = form.location.data
            if location == '':
                location: str = 'nil'
            category: str = form.category.data
            if category == '':
                category: str = 'nil'
            return redirect(url_for('personalised_events', keyword=keyword, location=location, category=category))
    search_terms = [keyword.lower(), location.lower(), category.lower()]
    events = Event.query.all()
    id_list = []
    for item in search_terms:
        if item == 'nil':
            continue
        for event in events:
            title=event.title.lower()
            description=event.description.lower()
            tags=event.tags.lower()
            event_location=event.location.lower()
            if item in title:
                id_list.append(event.id)
            if item in description:
                id_list.append(event.id)
            if item in tags:
                id_list.append(event.id)
            if item in event_location:
                id_list.append(event.id)
    if keyword !='nil':
        form.keyword.data = keyword
    if location !='nil':
        form.location.data = location
    if category !='nil':
        form.category.data = category
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter(Event.id.in_((id_list))).order_by(Event.date_posted.desc()).paginate(page=page, per_page=15)
    if events is None:
        print('Empty')
    return render_template('discover.html', login_form=login_form, regis_form=regis_form, form=form, events=events, search_form=search_form)


@app.route("/my_events", methods=['GET', 'POST'])
@login_required
def my_events():
    search_form = SearchForm(request.form, prefix="search-form")
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    user_email = current_user.email
    user = User.query.filter_by(email=user_email).first()
    notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
    if user.is_account_verified == False:
        return render_template('account_verification.html', search_form=search_form, regis_form=regis_form, login_form=login_form)
    events = Event.query.filter_by(event_author=user).order_by(Event.date_posted.desc())
    return render_template('my_events.html', events=events, notifcount=notifcount, msgcount=msgcount)

@app.route("/event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.event_author != current_user:
        abort(403)
    form = CreateEventForm()
    if form.validate_on_submit():
        user_email = current_user.email
        user = User.query.filter_by(email=user_email).first()
        event.title = form.title.data
        event.desc = form.description.data
        event.image1 = save_picture(form.image1.data)
        if form.image2.data:
            event.image2 = save_picture(form.image2.data)
        else:
            event.image2=''
        if form.image3.data:
            event.image3 = save_picture(form.image3.data)
        else:
            event.image3=''
        if form.image4.data:
            event.image4 = save_picture(form.image4.data)
        else:
            event.image4=''
        if form.image5.data:
            event.image5 = save_picture(form.image5.data)
        else:
            event.image5=''
        if form.image6.data:
            event.image6 = save_picture(form.image6.data)
        else:
            event.image6=''
        if form.image7.data:
            event.image7 = save_picture(form.image7.data)
        else:
            event.image7=''
        event.location = form.location.data
        event.price = form.price.data
        event.date = form.date.data
        event.date_end = form.date_end.data
        event.time = form.time.data
        event.time_end = form.time_end.data
        event.days = form.days.data
        event.pre_knowledge = form.pre_knowledge.data
        event.tags = form.tags.data
        event.schedule = form.schedule.data
        event.direction = form.direction.data
        event.equipment = form.equipment.data
        event.min_tickets = form.min_tickets.data
        event.offers_bool = form.offers_bool.data
        if form.attendee1:
            event.attendee1 = form.attendee1.data
            event.discount1 = form.discount1.data
        if form.attendee2:
            event.attendee2 = form.attendee2.data
            event.discount2 = form.discount2.data
        if form.attendee3:
            event.attendee3 = form.attendee3.data
            event.discount3 = form.discount3.data
        if form.attendee4:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee5:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee6:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee7:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee8:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        event.fee_cancel = form.fee_cancel.data
        event.prioritize = form.prioritize.data
        db.session.commit()
        event_id = event.id
        flash('Your event has been updated!', 'success')
        return redirect(url_for('eventdashboard', event_id=event_id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.location.data = event.location
        form.price.data = event.price
        form.date.data = event.date
        form.date_end.data = event.date_end
        form.time.data = event.time
        form.time_end.data = event.time_end
        form.days.data = event.days
        form.pre_knowledge.data = event.pre_knowledge
        form.tags.data = event.tags
        form.schedule.data = event.schedule
        form.direction.data = event.direction
        form.equipment.data = event.equipment
        form.min_tickets.data = event.min_tickets
        form.image1.data = event.image1
        form.image2.data = event.image2
        form.image3.data = event.image3
        form.image4.data = event.image4
        form.image5.data = event.image5
        form.image6.data = event.image6
        form.image7.data = event.image7
        form.offers_bool.data = event.offers_bool
        form.attendee1.data = event.attendee1
        form.attendee2.data = event.attendee2
        form.attendee3.data = event.attendee3
        form.attendee4.data = event.attendee4
        form.attendee5.data = event.attendee5
        form.attendee6.data = event.attendee6
        form.attendee7.data = event.attendee7
        form.attendee8.data = event.attendee8
        form.discount1.data = event.discount1
        form.discount2.data = event.discount2
        form.discount3.data = event.discount3
        form.discount4.data = event.discount4
        form.discount5.data = event.discount5
        form.discount6.data = event.discount6
        form.discount7.data = event.discount7
        form.discount8.data = event.discount8
        form.prioritize.data = event.prioritize
        form.fee_cancel.data = event.fee_cancel
    return render_template('update_event.html', title='Update Event', form=form, event=event)

@app.route("/admin-event/<int:event_id>/update", methods=['GET', 'POST'])
@login_required
def admin_update_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.id != 1:
        abort(403)
    form = CreateEventForm()
    if form.validate_on_submit():
        user_email = current_user.email
        user = User.query.filter_by(email=user_email).first()
        event.title = form.title.data
        event.desc = form.description.data
        event.image1 = save_picture(form.image1.data)
        if form.image2.data:
            event.image2 = save_picture(form.image2.data)
        else:
            event.image2=''
        if form.image3.data:
            event.image3 = save_picture(form.image3.data)
        else:
            event.image3=''
        if form.image4.data:
            event.image4 = save_picture(form.image4.data)
        else:
            event.image4=''
        if form.image5.data:
            event.image5 = save_picture(form.image5.data)
        else:
            event.image5=''
        if form.image6.data:
            event.image6 = save_picture(form.image6.data)
        else:
            event.image6=''
        if form.image7.data:
            event.image7 = save_picture(form.image7.data)
        else:
            event.image7=''
        event.location = form.location.data
        event.price = form.price.data
        event.date = form.date.data
        event.date_end = form.date_end.data
        event.time = form.time.data
        event.time_end = form.time_end.data
        event.days = form.days.data
        event.pre_knowledge = form.pre_knowledge.data
        event.tags = form.tags.data
        event.schedule = form.schedule.data
        event.direction = form.direction.data
        event.equipment = form.equipment.data
        event.min_tickets = form.min_tickets.data
        event.offers_bool = form.offers_bool.data
        if form.attendee1:
            event.attendee1 = form.attendee1.data
            event.discount1 = form.discount1.data
        if form.attendee2:
            event.attendee2 = form.attendee2.data
            event.discount2 = form.discount2.data
        if form.attendee3:
            event.attendee3 = form.attendee3.data
            event.discount3 = form.discount3.data
        if form.attendee4:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee5:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee6:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee7:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        if form.attendee8:
            event.attendee4 = form.attendee4.data
            event.discount4 = form.discount4.data
        event.fee_cancel = form.fee_cancel.data
        event.prioritize = form.prioritize.data
        db.session.commit()
        event_id = event.id
        flash('Event has been updated!', 'success')
        return redirect(url_for('eventdashboard', event_id=event_id))
    elif request.method == 'GET':
        form.title.data = event.title
        form.description.data = event.description
        form.location.data = event.location
        form.price.data = event.price
        form.date.data = event.date
        form.date_end.data = event.date_end
        form.time.data = event.time
        form.time_end.data = event.time_end
        form.days.data = event.days
        form.pre_knowledge.data = event.pre_knowledge
        form.tags.data = event.tags
        form.schedule.data = event.schedule
        form.direction.data = event.direction
        form.equipment.data = event.equipment
        form.min_tickets.data = event.min_tickets
        form.image1.data = event.image1
        form.image2.data = event.image2
        form.image3.data = event.image3
        form.image4.data = event.image4
        form.image5.data = event.image5
        form.image6.data = event.image6
        form.image7.data = event.image7
        form.offers_bool.data = event.offers_bool
        form.attendee1.data = event.attendee1
        form.attendee2.data = event.attendee2
        form.attendee3.data = event.attendee3
        form.attendee4.data = event.attendee4
        form.attendee5.data = event.attendee5
        form.attendee6.data = event.attendee6
        form.attendee7.data = event.attendee7
        form.attendee8.data = event.attendee8
        form.discount1.data = event.discount1
        form.discount2.data = event.discount2
        form.discount3.data = event.discount3
        form.discount4.data = event.discount4
        form.discount5.data = event.discount5
        form.discount6.data = event.discount6
        form.discount7.data = event.discount7
        form.discount8.data = event.discount8
        form.prioritize.data = event.prioritize
        form.fee_cancel.data = event.fee_cancel
    return render_template('admin_update_event.html', title='Update Event', form=form, event=event)

@app.route("/event/<int:event_id>/delete")
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.event_author != current_user:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('dashboard'))

@app.route("/admin-event/<int:event_id>/delete")
@login_required
def admin_delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    if current_user.id != 1:
        abort(403)
    db.session.delete(event)
    db.session.commit()
    flash('Event has been deleted!', 'success')
    return redirect(url_for('admin'))

@app.route("/event/<int:event_id>/enable", methods=['POST'])
@login_required
def enable_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.event_author != current_user:
        abort(403)
    event.is_enabled = True
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('event', event_id=event.id))

@app.route("/event/<int:event_id>/disable", methods=['POST'])
@login_required
def disable_event(event_id):
    event = Event.query.get_or_404(event_id)
    if event.event_author != current_user:
        abort(403)
    event.is_enabled = False
    db.session.commit()
    flash('Your event has been deleted!', 'success')
    return redirect(url_for('event', event_id=event.id))

@app.route("/event/<int:event_id>")
def event(event_id):
    event = Event.query.get_or_404(event_id)
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    msg_form = CreatorMsgForm(request.form, prefix="creatormsg-form")
    return render_template('event.html', title=event.title, event=event, login_form=login_form, regis_form=regis_form, search_form=search_form, msg_form=msg_form)

@app.route("/eventdashboard/<int:event_id>")
@login_required
def eventdashboard(event_id):
    user = User.query.filter_by(email=current_user.email).first()
    event = Event.query.get_or_404(event_id)
    if user.id != event.creator_id:
        abort(404)
    return render_template('eventdashboard.html', event=event)

@app.route("/event-reviews/<int:event_id>")
@login_required
def event_reviews(event_id):
    user = User.query.filter_by(email=current_user.email).first()
    event = Event.query.get_or_404(event_id)
    if user.id != event.creator_id:
        abort(404)
    return render_template('eventreviews.html', event=event)

@app.route("/event-faqs/<int:event_id>")
@login_required
def event_faqs(event_id):
    user = User.query.filter_by(email=current_user.email).first()
    event = Event.query.get_or_404(event_id)
    if user.id != event.creator_id:
        abort(404)
    return render_template('eventfaqs.html', event=event)

@app.route("/attendees")
@login_required
def attendees():
    user = User.query.filter_by(email=current_user.email).first()
    events = Event.query.filter_by(creator_id=user.id).all()
    return render_template('attendees.html', events=events)

@app.route("/booked-events")
@login_required
def booked_events():
    user = User.query.filter_by(email=current_user.email).first()
    bookings = Booking.query.filter_by(user_id=user.id).all()
    id_list = []
    for item in bookings:
        id_list.append(item.event_id)
    events = Event.query.filter(Event.id.in_((id_list))).order_by(Event.date_posted.desc()).all()
    return render_template('booked_events.html', events=events)

@app.route("/user-reviews")
@login_required
def user_reviews():
    return render_template('user_reviews.html')

@app.route("/admin-creators")
@login_required
def admin_creators():
    if current_user.id != 1:
        abort(403)
    page = request.args.get('page', 1, type=int)
    creators = User.query.filter_by(is_creator=True).order_by(User.id.desc()).paginate(page=page, per_page=15)
    return render_template('admin_creators.html', creators=creators)

@app.route("/admin-users")
@login_required
def admin_users():
    if current_user.id != 1:
        abort(403)
    page = request.args.get('page', 1, type=int)
    users = User.query.order_by(User.id.desc()).paginate(page=page, per_page=15)
    return render_template('admin_users.html', users=users)

@app.route("/admin-events")
@login_required
def admin_events():
    if current_user.id != 1:
        abort(403)
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.id.desc()).paginate(page=page, per_page=15)
    return render_template('admin_events.html', events=events)

@app.route("/admin-creator-events/<int:user_id>")
@login_required
def admin_creator_events(user_id):
    if current_user.id != 1:
        abort(403)
    user = User.query.filter_by(id=user_id).first()
    page = request.args.get('page', 1, type=int)
    events = Event.query.filter_by(creator_id=user.id).order_by(Event.id.desc()).paginate(page=page, per_page=15)
    return render_template('admin_creator_events.html', events=events , user=user)

@app.route("/credits")
@login_required
def credits():
    return render_template('credits.html')


@app.route("/creator-reviews")
@login_required
def creator_reviews():
    return render_template('creator_reviews.html')


@app.route("/user/<string:username>")
def user_events(username):
    user = User.query.filter_by(username=username).first_or_404()
    events = Event.query.filter_by(event_author=user).order_by(Event.date_posted.desc())
    notifcount = Notification.query.filter_by(user_id=user.id, read=False).count()
    msgcount = Messages.query.filter_by(receiver=user.id, read=False).count()
    return render_template('user_events.html', events=events, user=user, notifcount=notifcount, msgcount=msgcount)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def verifi_account():
    verifi = 0
    if current_user.is_authenticated:
        user_email = current_user.email
        user = User.query.filter_by(email=user_email).first()
        if user.verified_account is False:
            verifi = 1
            return verifi
    return verifi


# -----------------------------------------------------------------------------------


# -------------------------------------Password Reset---------------------------------


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('home'))
    return render_template('reset_request.html', title='Reset Password', form=form, login_form=login_form, regis_form=regis_form,search_form=search_form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    login_form = LoginForm(request.form, prefix="login-form")
    regis_form = RegistrationForm(request.form, prefix="register-form")
    search_form = SearchForm(request.form, prefix="search-form")
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('home'))
    return render_template('reset_token.html', title='Reset Password', form=form, login_form=login_form, regis_form=regis_form,search_form=search_form)


# -----------------------------------------------------------------------------------------


# --------------------------------------Email Account Verification---------------------------------


def send_verify_account_email(user):
    token = user.get_verify_account_token()
    msg = Message('Email Verification',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To activate your account, visit the following link:
{url_for('verification_token', token=token, _external=True)}
If you did not make this request then simply ignore this email.
'''
    mail.send(msg)


@app.route("/email_verification", methods=['GET', 'POST'])
def verify_email():
    if current_user.is_authenticated:
        user_email = current_user.email
        user = User.query.filter_by(email=user_email).first()
        if user.is_account_verified is False:
            user_email = current_user.email
            user = User.query.filter_by(email=user_email).first()
            send_verify_account_email(user)
            flash(f'An email has been sent to {user_email} with instructions to activate your account.', 'info')
            return redirect(url_for('home'))
    return redirect(url_for('home'))


@app.route("/verify_email/<token>", methods=['GET', 'POST'])
def verification_token(token):
    user = User.verify_account_verification_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('home'))
    if user.is_account_verified is False:
        user.is_account_verified = True
        db.session.commit()
        flash('Your account has been verified!', 'success')
        return redirect(url_for('account_details'))
    return redirect(url_for('home'))