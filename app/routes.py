import qrcode
import os
import uuid
from flask import render_template, flash, redirect, url_for, request, session, jsonify, send_file
from flask_login import login_user, logout_user, current_user, login_required
from app.forms import LoginForm, AddClientForm, AddGrowerForm, AddVarietyForm, AddRawMaterialPackagingForm, RawMaterialReceptionForm, LotForm, FullTruckWeightForm, LotQCForm
from app.models import User, Client, Grower, Variety, RawMaterialPackaging, RawMaterialReception, Lot, FullTruckWeight, LotQC
from app import app, db
from io import BytesIO
from datetime import datetime
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            session.permanent = True
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        else:
            flash('Invalid email or password')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/add_client', methods=['GET', 'POST'])
def add_client():
    form = AddClientForm()
    if form.validate_on_submit():
        client = Client(
            name=form.name.data,
            tax_id=form.tax_id.data,
            address=form.address.data,
            comuna=form.comuna.data)
        db.session.add(client)
        db.session.commit()
        flash('Client added successfully!', 'success')
        return redirect(url_for('index'))  # Redirect to the index page or wherever appropriate
    return render_template('add_client.html', title='Add Client', form=form)

@app.route('/list_clients')
def list_clients():
    clients = Client.query.all()
    return render_template('list_clients.html', clients=clients)

@app.route('/add_grower', methods=['GET', 'POST'])
def add_grower():
    form = AddGrowerForm()
    if form.validate_on_submit():
        grower = Grower(
            name=form.name.data,
            tax_id=form.tax_id.data,
            csg_code=form.csg_code.data)
        db.session.add(grower)
        db.session.commit()
        flash('Grower added successfully!')
        return redirect(url_for('list_growers'))
    return render_template('add_grower.html', form=form)

@app.route('/list_growers')
def list_growers():
    growers = Grower.query.all()
    return render_template('list_growers.html', growers=growers)

@app.route('/add_variety', methods=['GET', 'POST'])
def add_variety():
    form = AddVarietyForm()
    if form.validate_on_submit():
        variety = Variety(
            name=form.name.data)
        db.session.add(variety)
        db.session.commit()
        flash('Variety added successfully!')
        return redirect(url_for('list_varieties'))
    return render_template('add_variety.html', form=form)

@app.route('/list_varieties')
def list_varieties():
    varieties = Variety.query.all()
    return render_template('list_varieties.html', varieties=varieties)

@app.route('/add_raw_material_packaging', methods=['GET', 'POST'])
def add_raw_material_packaging():
    form = AddRawMaterialPackagingForm()
    if form.validate_on_submit():
        rmp = RawMaterialPackaging(
            name=form.name.data,
            tare=form.tare.data)
        db.session.add(rmp)
        db.session.commit()
        flash('Envase agregado correctamente!')
        return redirect(url_for('list_raw_material_packagings'))
    return render_template('add_raw_material_packaging.html', form=form)

@app.route('/list_raw_material_packagins')
def list_raw_material_packagings():
    rmps = RawMaterialPackaging.query.all()
    return render_template('list_raw_material_packagings.html', rmps=rmps)

@app.route('/add_raw_material_reception', methods=['GET', 'POST'])
def add_raw_material_reception():
    form = RawMaterialReceptionForm()
    if form.validate_on_submit():
        reception = RawMaterialReception(
            waybill=form.waybill.data,
            date=form.date.data,
            time=form.time.data,
            truck_plate=form.truck_plate.data,
            trucker_name=form.trucker_name.data
        )

        selected_grower = Grower.query.get(form.grower_id.data)
        selected_client = Client.query.get(form.client_id.data)
        if selected_grower:
            reception.growers.append(selected_grower)
        if selected_client:
            reception.clients.append(selected_client)

        db.session.add(reception)
        db.session.commit()
        flash('Raw Material Reception added successfully!')
        return redirect(url_for('create_lot', reception_id=reception.id))

    return render_template('add_raw_material_reception.html', form=form)

@app.route('/create_lot/<int:reception_id>', methods=['GET', 'POST'])
def create_lot(reception_id):
    form = LotForm()
    if request.method == 'GET':
        reception = RawMaterialReception.query.get_or_404(reception_id)
        form.grower_name.data = ', '.join([grower.name for grower in reception.growers])
        form.client_name.data = ', '.join([client.name for client in reception.clients])
        form.waybill.data = reception.waybill
    if form.validate_on_submit():
        # This checks if the form submission was caused by the 'create_another' button
        if 'submit' in request.form:
            lot = Lot(
                rawmaterialreception_id=reception_id,
                variety_id=form.variety_id.data,
                rawmaterialpackaging_id=form.rawmaterialpackaging_id.data,
                packagings_quantity=form.packagings_quantity.data,
                lot_number=form.lot_number.data
            )
            db.session.add(lot)
            db.session.commit()
            flash('Lot created successfully.', 'success')
            return redirect(url_for('create_lot', reception_id=reception_id))

    return render_template('create_lot.html', form=form)

@app.route('/full_truck_weight/<int:lot_id>', methods=['GET', 'POST'])
def full_truck_weight(lot_id):
    lot = Lot.query.get_or_404(lot_id)
    form = FullTruckWeightForm()

    if form.validate_on_submit():
        full_truck_weight = FullTruckWeight(
            loaded_truck_weight=form.loaded_truck_weight.data,
            empty_truck_weight=form.empty_truck_weight.data,
            lot_id=lot_id
        )
        db.session.add(full_truck_weight)
        db.session.commit()

        # Calculate and update the net weight of the lot
        net_weight = full_truck_weight.loaded_truck_weight - full_truck_weight.empty_truck_weight - (lot.raw_material_packaging.tare * lot.packagings_quantity)
        lot.net_weight = net_weight
        db.session.commit()

        flash('Full truck weight and net weight registered successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('full_truck_weight.html', form=form, lot=lot)

@app.route('/select_lot_for_weight_registration')
def select_lot_for_weight_registration():
    lots = Lot.query.filter_by(net_weight=0).all()
    return render_template('select_lot_for_weight_registration.html', lots=lots)

@app.route('/register_full_truck_weight/<int:lot_id>', methods=['GET', 'POST'])
def register_full_truck_weight(lot_id):
    lot = Lot.query.get_or_404(lot_id)
    form = FullTruckWeightForm()

    if form.validate_on_submit():
        full_truck_weight = FullTruckWeight(
            loaded_truck_weight=form.loaded_truck_weight.data,
            empty_truck_weight=form.empty_truck_weight.data,
            lot_id=lot_id
        )
        db.session.add(full_truck_weight)
        
        packaging_tare = RawMaterialPackaging.query.get(lot.rawmaterialpackaging_id).tare

        lot.net_weight = (
            full_truck_weight.loaded_truck_weight - 
            full_truck_weight.empty_truck_weight - 
            (packaging_tare * lot.packagings_quantity)
        )
        
        db.session.commit()

        flash('Full truck weight registered successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('register_full_truck_weight.html', form=form, lot=lot)

@app.route('/process_selected_lot', methods=['POST'])
def process_selected_lot():
    selected_lot_id = request.form.get('selected_lot')

    if selected_lot_id:
        return redirect(url_for('full_truck_weight', lot_id=selected_lot_id))
    
    else:
        flash('No lot selected.', 'warning')
        return redirect(url_for('raw_material_receptions_weight_zero'))

@app.route('/generate_qr')
def generate_qr():
    # Receive the reception_id from the query parameters
    reception_id = request.args.get('reception_id', 'default')

    # Dynamically generate the URL for 'lot_net_details' route
    # _external=True generates an absolute URL, including the domain
    url = url_for('lot_net_details', reception_id=reception_id, _external=True)
    
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/create_lot_qc', methods=['GET', 'POST'])
def create_lot_qc():
    form = LotQCForm()
    if form.validate_on_submit():
        new_lot_qc = LotQC(
            lot_id=form.lot_id.data,
            analyst=form.analyst.data,
            date=form.date.data,
            time=form.time.data,
            units=form.units.data,
            inshell_weight=form.inshell_weight.data,
            shelled_weight=form.shelled_weight.data,
            yieldpercentage=form.yieldpercentage.data,
            lessthan30=form.lessthan30.data,
            between3032=form.between3032.data,
            between3234=form.between3234.data,
            between3436=form.between3436.data,
            morethan36=form.morethan36.data,
            broken_walnut=form.broken_walnut.data,
            split_walnut=form.split_walnut.data,
            light_stain=form.light_stain.data,
            serious_stain=form.serious_stain.data,
            adhered_hull=form.adhered_hull.data,
            shrivel=form.shrivel.data,
            empty=form.empty.data,
            insect_damage=form.insect_damage.data,
            inactive_fungus=form.inactive_fungus.data,
            active_fungus=form.active_fungus.data,
            extra_light=form.extra_light.data,
            light=form.light.data,
            light_amber=form.light_amber.data,
            amber=form.amber.data,
            yellow=form.yellow.data
        )

        def save_image(uploaded_file):
            if uploaded_file:
                original_name = secure_filename(uploaded_file.filename)
                timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
                unique_name = f"{uuid.uuid4()}_{timestamp}_{original_name}"
                relative_path = os.path.join('images', unique_name)
                full_path = os.path.join(app.config['UPLOAD_PATH_IMAGE'], unique_name)
                try:
                    uploaded_file.save(full_path)
                    flash(f'Image saved: {unique_name}', 'info')
                    return relative_path
                except Exception as e:
                    flash(f"Error saving file: {str(e)}", 'error')
                    return None
            else:
                flash('No file uploaded', 'warning')
                return None

        # Image upload handling
        inshell_image_path = save_image(form.inshell_image.data)
        shelled_image_path = save_image(form.shelled_image.data)
        
        if inshell_image_path and shelled_image_path:
            new_lot_qc.inshell_image_path = inshell_image_path
            new_lot_qc.shelled_image_path = shelled_image_path
            db.session.add(new_lot_qc)
            db.session.commit()
            flash('Lot QC record created successfully!', 'success')
        else:
            flash('Failed to save images. Please try again.', 'error')

        return redirect(url_for('index'))
    else:
        for fieldName, errorMessages in form.errors.items():
            for err in errorMessages:
                flash(f'Error in {fieldName}: {err}', 'error')

    return render_template('create_lot_qc.html', form=form)

@app.route('/lot_qc_reports')
def lot_qc_reports():
    lot_qc_records = LotQC.query.all()  # Assuming LotQC is your model name
    return render_template('lot_qc_reports.html', lot_qc_records=lot_qc_records)

@app.route('/view_lot_qc_report/<int:report_id>')
def view_lot_qc_report(report_id):
    report = LotQC.query.get_or_404(report_id)
    lot = report.lot
    reception = lot.raw_material_reception
    clients = reception.clients
    growers = reception.growers

    return render_template('view_lot_qc_report.html', report=report, reception=reception, clients=clients, growers=growers)


