from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, PasswordField, SelectField, DateField, TimeField, SubmitField, HiddenField, RadioField, BooleanField
from wtforms.validators import DataRequired, InputRequired, ValidationError, Length, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired
from app.models import User, Role, Client, Grower, Variety, RawMaterialPackaging, Lot

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

class RawMaterialReceptionForm(FlaskForm):
    waybill = StringField('Guía Nº', validators=[DataRequired(), Length(max=64)])
    date = DateField('Fecha', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Hora', validators=[DataRequired()], format='%H:%M')
    truck_plate = StringField('Patente', validators=[DataRequired(), Length(max=6)])
    trucker_name = StringField('Chofer', validators=[Length(max=64)])

    # Dynamic choice fields for Grower and Client
    grower_id = SelectField('Productor', coerce=int, validators=[DataRequired()])
    client_id = SelectField('Cliente', coerce=int, validators=[DataRequired()])

    submit = SubmitField('Crear Recepción')

    def __init__(self, *args, **kwargs):
        super(RawMaterialReceptionForm, self).__init__(*args, **kwargs)
        self.grower_id.choices = [(g.id, g.name) for g in Grower.query.all()]
        self.client_id.choices = [(c.id, c.name) for c in Client.query.all()]

class LotForm(FlaskForm):
    reception_id = HiddenField('Reception ID')  # This remains hidden and carries the actual reception ID
    grower_name = StringField('Productor', render_kw={'readonly': True})
    client_name = StringField('Cliente', render_kw={'readonly': True})
    waybill = StringField('Guía de Despacho Nº', render_kw={'readonly': True})
    variety_id = SelectField('Variedad', coerce=int, validators=[DataRequired()])
    rawmaterialpackaging_id = SelectField('Tipo de Envases', coerce=int, validators=[DataRequired()])
    packagings_quantity = IntegerField('Cantidad de Envases', validators=[DataRequired()])
    lot_number = IntegerField('Número de Lote', validators=[DataRequired()])

    def __init__(self, *args, **kwargs):
        super(LotForm, self).__init__(*args, **kwargs)
        self.variety_id.choices = [(v.id, v.name) for v in Variety.query.all()]
        self.rawmaterialpackaging_id.choices = [(p.id, p.name) for p in RawMaterialPackaging.query.all()]

    submit = SubmitField('Crear Lote')

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
    inshell_image = FileField('Imagen de Cáscara', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    shelled_image = FileField('Imagen de Pulpa', validators=[FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    lot_id = SelectField('Lote', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super(LotQCForm, self).__init__(*args, **kwargs)
        self.lot_id.choices = [(l.id, l.lot_number) for l in Lot.query.all()]

    def validate_shelled_weight(self, field):
        total_color_weight = self.extra_light.data + self.light.data + self.light_amber.data + self.amber.data # type: ignore
        if field.data != total_color_weight:
            raise ValidationError('El peso de pulpa debe ser igual a la suma de los pesos de los colores.')