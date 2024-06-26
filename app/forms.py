from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, PasswordField, SelectField, SelectMultipleField, DateField, TimeField, SubmitField, HiddenField, RadioField, BooleanField
from wtforms.validators import DataRequired, InputRequired, ValidationError, Length, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User, Role, Area, Client, Grower, Variety, RawMaterialPackaging, Lot

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])

    submit = SubmitField('Ingresar')

class AddUserForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_number = StringField('Celular', validators=[DataRequired(), Length(min=9, max=9)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Agregar Usuario')

class AddRoleForm(FlaskForm):
    name = StringField('Rol', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Agregar Rol')

class AddAreaForm(FlaskForm):
    name = StringField('Area', validators=[DataRequired()])
    description = StringField('Descripción', validators=[DataRequired()])
    submit = SubmitField('Agregar Area')

class AssignRoleForm(FlaskForm):
    user_id = SelectField('Usuario', coerce=int, validators=[DataRequired()])
    role_id = SelectField('Rol', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Rol')

    def __init__(self, *args, **kwargs):
        super(AssignRoleForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.email) for u in User.query.order_by(User.email).all()]
        self.role_id.choices = [(r.id, r.name) for r in Role.query.order_by(Role.name).all()]

class AssignAreaForm(FlaskForm):
    user_id = SelectField('Usuario', coerce=int, validators=[DataRequired()])
    area_id = SelectField('Area', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Asignar Area')

    def __init__(self, *args, **kwargs):
        super(AssignAreaForm, self).__init__(*args, **kwargs)
        self.user_id.choices = [(u.id, u.email) for u in User.query.order_by(User.email).all()]
        self.area_id.choices = [(r.id, r.name) for r in Area.query.order_by(Area.name).all()]

class AddClientForm(FlaskForm):
    name = StringField('Razón Social', validators=[DataRequired()])
    tax_id = StringField('Rut', validators=[DataRequired()])
    address = StringField('Dirección', validators=[DataRequired()])
    comuna = StringField('Comuna', validators=[DataRequired()])
    submit = SubmitField('Agregar Cliente')

class AddGrowerForm(FlaskForm):
    name = StringField('Razón Social', validators=[DataRequired()])
    tax_id = StringField('Rut', validators=[DataRequired()])
    csg_code = StringField('Código CSG', validators=[DataRequired()])
    submit = SubmitField('Agregar Productor')

class AddVarietyForm(FlaskForm):
    name = StringField('Variedad', validators=[DataRequired()])
    submit = SubmitField('Agregar Variedad')

class AddRawMaterialPackagingForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired()])
    tare = FloatField('Tara', validators=[DataRequired()])
    submit = SubmitField('Agregar Envase de MP')

class CreateRawMaterialReceptionForm(FlaskForm):
    waybill = IntegerField('Guía Nº', validators=[DataRequired()])
    date = DateField('Fecha', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Hora', validators=[DataRequired()], format='%H:%M')
    truck_plate = StringField('Patente', validators=[DataRequired(), Length(max=6)])
    trucker_name = StringField('Chofer', validators=[Length(max=64)])
    observations = TextAreaField('Observaciones', validators=[Length(max=255)])

    # Dynamic choice fields for Grower and Client
    grower_id = SelectField('Productor', coerce=int, validators=[DataRequired()])
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Crear Recepción')

    def __init__(self, *args, **kwargs):
        super(CreateRawMaterialReceptionForm, self).__init__(*args, **kwargs)
        self.grower_id.choices = [(g.id, g.name) for g in Grower.query.all()]
        self.client_id.choices = [(c.id, c.name) for c in Client.query.all()]

class CreateLotForm(FlaskForm):
    reception_id = HiddenField('Reception ID')
    grower_name = StringField('Productor', render_kw={'readonly': True})
    client_name = StringField('Cliente', render_kw={'readonly': True})
    waybill = StringField('Guía de Despacho Nº', render_kw={'readonly': True})
    variety_id = SelectField('Variedad', coerce=int, validators=[DataRequired()])
    rawmaterialpackaging_id = SelectField('Tipo de Envases', coerce=int, validators=[DataRequired()])
    packagings_quantity = IntegerField('Cantidad de Envases', validators=[DataRequired()])
    lot_number = IntegerField('Número de Lote', validators=[DataRequired()])
    submit = SubmitField('Crear Lote')

    def __init__(self, *args, **kwargs):
        super(CreateLotForm, self).__init__(*args, **kwargs)
        self.variety_id.choices = [(v.id, v.name) for v in Variety.query.all()]
        self.rawmaterialpackaging_id.choices = [(p.id, p.name) for p in RawMaterialPackaging.query.all()]

class FullTruckWeightForm(FlaskForm):
    loaded_truck_weight = FloatField('Loaded Truck Weight', validators=[DataRequired()])
    empty_truck_weight = FloatField('Empty Truck Weight', validators=[DataRequired()])
    submit = SubmitField('Register')

class LotQCForm(FlaskForm):
    analyst = StringField('Analista', validators=[DataRequired(), Length(max=64)])
    date = DateField('Fecha', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Hora', validators=[DataRequired()], format='%H:%M')
    units = IntegerField('Unidades Analizadas', validators=[InputRequired()])
    inshell_weight = FloatField('Peso Con Cáscara', validators=[InputRequired()])
    shelled_weight = FloatField('Peso de Pulpa', validators=[InputRequired()])
    yieldpercentage = FloatField('Porcentaje de Pulpa', validators=[InputRequired()])
    lessthan30 = IntegerField('Menos de 30', validators=[InputRequired()])
    between3032 = IntegerField('30/32', validators=[InputRequired()])
    between3234 = IntegerField('32/34', validators=[InputRequired()])
    between3436 = IntegerField('34/36', validators=[InputRequired()])
    morethan36 = IntegerField('Más de 36', validators=[InputRequired()])
    broken_walnut = IntegerField('Cáscara Partida', validators=[InputRequired()])
    split_walnut = IntegerField('Casco Abierto', validators=[InputRequired()])
    light_stain = IntegerField('Mancha Leve', validators=[InputRequired()])
    serious_stain = IntegerField('Mancha Grave', validators=[InputRequired()])
    adhered_hull = IntegerField('Pelón Adherido', validators=[InputRequired()])
    shrivel = IntegerField('Nuez Reseca', validators=[InputRequired()])
    empty = IntegerField('Nuez Vana', validators=[InputRequired()])
    insect_damage = IntegerField('Daño de Insecto', validators=[InputRequired()])
    inactive_fungus = IntegerField('Hongo Inactivo', validators=[InputRequired()])
    active_fungus = IntegerField('Hongo Activo', validators=[InputRequired()])
    extra_light = FloatField('Extra Light', validators=[InputRequired()])
    light = FloatField('Light', validators=[InputRequired()])
    light_amber = FloatField('Light Amber', validators=[InputRequired()])
    amber = FloatField('Amber', validators=[InputRequired()])
    yellow = FloatField('Amarilla', validators=[InputRequired()])
    inshell_image = FileField('Imagen de Cáscara', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes Solamente!')])
    shelled_image = FileField('Imagen de Pulpa', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes Solamente!')])
    lot_id = SelectField('Lote', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Crear QC')

    def __init__(self, *args, **kwargs):
        super(LotQCForm, self).__init__(*args, **kwargs)
        self.lot_id.choices = [(l.id, l.lot_number) for l in Lot.query.all()]

    def validate_shelled_weight(self, field):
        total_color_weight = self.extra_light.data + self.light.data + self.light_amber.data + self.amber.data # type: ignore
        if field.data != total_color_weight:
            raise ValidationError('El peso de pulpa debe ser igual a la suma de los pesos de los colores.')
        
class SampleQCForm(FlaskForm):
    grower = StringField('Productor', validators=[DataRequired(), Length(max=64)])
    variety = StringField('Variedad', validators=[DataRequired(), Length(max=64)])
    brought_by = StringField('Muestra traida por', validators=[DataRequired(), Length(max=64)])
    analyst = StringField('Analista', validators=[DataRequired(), Length(max=64)])
    date = DateField('Fecha', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Hora', validators=[DataRequired()], format='%H:%M')
    units = IntegerField('Unidades Analizadas', validators=[InputRequired()])
    inshell_weight = IntegerField('Peso Con Cáscara', validators=[InputRequired()], render_kw={"id": "inshell_weight"})
    shelled_weight = IntegerField('Peso de Pulpa', validators=[InputRequired()], render_kw={"id": "shelled_weight"})
    yieldpercentage = FloatField('Porcentaje de Pulpa', validators=[InputRequired()], render_kw={"id": "yieldpercentage", "readonly": True})
    lessthan30 = IntegerField('Menos de 30', validators=[InputRequired()], render_kw={"id": "lessthan30"})
    between3032 = IntegerField('30/32', validators=[InputRequired()], render_kw={"id": "between3032"})
    between3234 = IntegerField('32/34', validators=[InputRequired()], render_kw={"id": "between3234"})
    between3436 = IntegerField('34/36', validators=[InputRequired()], render_kw={"id": "between3436"})
    morethan36 = IntegerField('Más de 36', validators=[InputRequired()], render_kw={"id": "morethan36"})
    broken_walnut = IntegerField('Cáscara Partida', validators=[InputRequired()])
    split_walnut = IntegerField('Casco Abierto', validators=[InputRequired()])
    light_stain = IntegerField('Mancha Leve', validators=[InputRequired()])
    serious_stain = IntegerField('Mancha Grave', validators=[InputRequired()])
    adhered_hull = IntegerField('Pelón Adherido', validators=[InputRequired()])
    shrivel = IntegerField('Nuez Reseca', validators=[InputRequired()])
    empty = IntegerField('Nuez Vana', validators=[InputRequired()])
    insect_damage = IntegerField('Daño de Insecto', validators=[InputRequired()])
    inactive_fungus = IntegerField('Hongo Inactivo', validators=[InputRequired()])
    active_fungus = IntegerField('Hongo Activo', validators=[InputRequired()])
    extra_light = FloatField('Extra Light', validators=[InputRequired()], render_kw={"id": "extra_light"})
    light = FloatField('Light', validators=[InputRequired()], render_kw={"id": "light"})
    light_amber = FloatField('Light Amber', validators=[InputRequired()], render_kw={"id": "light_amber"})
    amber = FloatField('Amber', validators=[InputRequired()], render_kw={"id": "amber"})
    yellow = FloatField('Amarilla', validators=[InputRequired()], render_kw={"id": "yellow"})
    inshell_image = FileField('Imagen de Cáscara', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes Solamente!')], render_kw={'id': 'inshell_image', 'class': 'form-control'})
    shelled_image = FileField('Imagen de Pulpa', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Imágenes Solamente!')], render_kw={'id': 'shelled_image', 'class': 'form-control'})
    submit = SubmitField('Crear QC')

    def validate_shelled_weight(self, field):
        total_color_weight = self.extra_light.data + self.light.data + self.light_amber.data + self.amber.data # type: ignore
        if field.data != total_color_weight:
            raise ValidationError('El peso de pulpa debe ser igual a la suma de los pesos de los colores.')
        
class FumigationForm(FlaskForm):
    work_order = StringField('Orden de Trabajo', validators=[DataRequired()])
    start_date = DateField('Fecha de Inicio', validators=[DataRequired()], format='%d-%m-%Y')
    start_time = TimeField('Hora de Inicio', validators=[DataRequired()], format='%H:%M')
    work_order_doc = FileField('Orden de Trabajo', validators=[FileRequired(), FileAllowed(['pdf'], 'Sólo PDF!')])
    lot_selection = SelectMultipleField('Lotes', coerce=int, choices=[])
    submit = SubmitField('Crear Fumigación')

    def __init__(self, *args, **kwargs):
        super(FumigationForm, self).__init__(*args, **kwargs)
        # Filter lots where fumigation_status is '2'
        sorted_lots = Lot.query.filter_by(fumigation_status='1').order_by(Lot.lot_number).all()
        self.lot_selection.choices = [(lot.id, f'Lote Nº {lot.lot_number}') for lot in sorted_lots]