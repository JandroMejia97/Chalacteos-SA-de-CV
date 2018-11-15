function mostrar(id) {
    if(document.getElementById){
        var ele =  document.getElementById(id);
        ele.style.display = (ele.style.display == 'none') ? 'block':'none';
    }
}
function disableField() {            
    document.getElementById("field-me").disabled = true;
    document.getElementById("save-me").disabled = true;
    document.getElementById("edit-me").disabled = false;
}

function undisableField() {
    document.getElementById("field-me").disabled = false;
    document.getElementById("save-me").disabled = false;
    document.getElementById("edit-me").disabled = true;
}
function validar_selector(selector, error_span){
    var i;
    var val = 1;
    for(i=0;i<selector.length;i++){
        if(selector[i] == null || selector[i] <= 0){
            error_span.innerHTML = "Debes seleccionar un país y una ciudad";
            error_span.hidden = false;
            console.log('SelectErrr');
            val = 0;
        }
    }
    return val;
}

function validar_text_input(input, error_span){
    var i;
    var val = 1;
    for(i=0;i<input.length;i++){
        if(input[i] == null || input[i].length == 0 || /s+S/.test(input[i])){
            error_span.innerHTML = "Rellena todos los campos de texto, Math.sin espacios iniciales"
            error_span.hidden = false;
            console.log('TextErro');
            val = 0;
        }
    }
    return val;
}
function validar_number_input(inputs, error_span){
    var i;
    var val = 1;
    for(i=0;i<inputs.length;i++){
        if(inputs[i] == null || inputs[i].length == 0 || isNaN(inputs[i])){
            error_span.innerHTML = "Rellena todos los campos numéricos"
            error_span.hidden = false;
            console.log('NumericoErro');
            val = 0;
        }
    }
    return val;
}
function obtener_datos(){
    var titulo = document.getElementById('titulo').value;
    var pais = document.getElementById('id_pais').value;
    var ciudad = document.getElementById('id_ciudad').value;
    var date_range = document.getElementById('date_range').value;
    var li_temp = document.getElementById('li_temperatura').value;
    var ls_temp = document.getElementById('ls_temperatura').value;
    var comentario = document.getElementById('comentario').value;
    var modelo_lente = document.getElementById('modelo_lente').value;
    var area_lente = document.getElementById('area_lente').value;
    var transmitancia = document.getElementById('id_transmitancia').value;
    var modelo_panel = document.getElementById('modelo_panel').value;
    var area_panel = document.getElementById('area_panel').value;
    var emisividad = document.getElementById('emisividad').value;
    var eficiencia = document.getElementById('eficiencia').value;
    var localidad = document.getElementById('localidad').value;
    //var datos_clima = document.getElementById('tipo_clima').value
    var error_span = document.getElementById("form_error");
    var exito_span = document.getElementById("form_exito");

    console.log(datos_clima);
    console.log(localidad);
    var form = document.getElementById('nueva');

    var text_inputs =  [titulo, comentario, date_range, modelo_lente, modelo_panel];
    var selectors = [pais, ciudad];
    var num_inputs = [li_temp, ls_temp, area_lente, area_panel, transmitancia, emisividad, eficiencia];
    var sel = validar_selector(selectors, error_span);
    console.log(sel.toString());
    var txt = validar_text_input(text_inputs, error_span);
    console.log(txt.toString());
    var num = validar_number_input(num_inputs, error_span);
    console.log(num.toString());
    if(sel == true && txt == true && num == true){
        error_span.hidden = true;
        if(li_temp >= ls_temp){
            error_span.innerHTML = "El limite inferior no debe ser mayor o igual al limite superior"
            error_span.hidden = false;
        }else{
            exito_span.innerHTML = "Datos ingresados correctamente"
            exito_span.hidden = false;
            
            date_range = date_range.split(' - ');

            fecha_inicial = new Date(date_range[0]);
            fecha_final = new Date(date_range[1]);
            
            dia_inicial = dias_diff(fecha_inicial);
            dia_final = dias_diff(fecha_final);

            /* datos = {
                fecha_final: 'fecha_final', fecha_inicial: 'fecha_inicial', 
                dia_inicial: 'dia_inicial', dia_final: 'dia_final', 
                titulo: 'titulo', comentario: 'comentario', 
                modelo_lente: 'modelo_lente', modelo_panel: 'modelo_panel',
                pais: 'pais', ciudad: 'ciudad',
                li_temp, ls_temp, 
                area_lente, area_panel, 
                transmitancia, emisividad, 
                eficiencia
            } */
        }
        return true;
    }
    modelo_lente.value = "HOLA MUNDO";

    var date_range = date_range.split(" - ");

    alert('Ingreso exitoso');
}
function dias_diff(d){
    var year = d.getFullYear();
    var fecha_base = new Date(year, 1, 1, 0, 0, 0, 0).getMilliseconds();
    d = d.getMilliseconds();
    diff = (d - fecha_base)/(1000*60*60*24);
    return diff;
}

window.onload = function () {
    mostrar('contenido');
};

class Angulo{
    
    constructor(latitud, dia_n){
        this.declinacion = this.calcular_declinacion(
            dia_n
        );
        this.media_jornada = this.calcular_media_jornada(
            latitud,
            this.declinacion
        );
        this.duracion_dia = this.calcular_duracion(
            this.media_jornada
        );
        this.tiempo_orto = this.calcular_hora_orto(
            this.duracion_dia
        );
        this.tiempo_ocaso = this.calcular_hora_ocaso(
            this.duracion_dia
        );
        this.hora = this.calcular_hora(
            this.tiempo_orto,
            this.tiempo_ocaso
        );
        this.angulo_horario = this.calcular_horario(
            this.hora
        );
        this.angulo_cenital = this.calcular_cenital(
            latitud, 
            this.declinacion,
            this.angulo_horario,
        );
    }
    
    
    calcular_declinacion(dia_n){
        declinacion = -23.45*Math.cos(2*pi*(10+dia_n)/365);
        return (Math.PI/180)*(declinacion);
    }

    get declinacion(){
        return this.declinacion;
    }
    
    calcular_media_jornada(latitud, declinacion){
        media_jornada = Math.acos(-Math.tan(Math.pi*(latitud)/180)*Math.tan(declinacion));
        return media_jornada;
    }

    get media_jornada(){
        return this.media_jornada;
    }
    
    calcular_duracion(media_jornada){
        duracion = 2*(180/Math.PI)*(media_jornada)/15;
        return duracion;
    }

    get duracion(){
        return this.duracion;
    }
    
    calcular_hora_orto(duracion){
        tor = 12 - duracion/2;
        return tor;
    }

    get hora_orto(){
        return this.hora_orto;
    }
    
    calcular_hora_ocaso(duracion){
        toc = 12 + duracion/2;
        return toc;
    }

    get hora_ocaso(){
        return this.hora_ocaso;
    }
    
    calcular_hora(tor, toc){
        var hora=[];
        var val = Math.round(tor+10/360*100)/100;
        hora.push(val);
        i=0;
        while(val < toc){
            val = hora[i]+1/20;
            if(val < toc){
                hora.push(Math.round(val*100)/100);
                i+=1;
            }
        }
        return hora;
    }

    get hora(){
        return this.hora;
    }

    calcular_horario(hora){
        var horario = [];
        var h = 0;
        for(h=0; h < hora.length; h++){
            horario.push(Math.round((Math.PI/180)*(15*(hora[i]-12))*100)/100);
        }
        return horario;
    }

    get horario(){
        return this.horario;
    }
    
    calcular_cenital(latitud, declinacion, angulo_horario){
        var cenital = [];
        var h = 0;
        for(h=0; h < angulo_horario.length ; h++){
            cenital.push(Math.round(Math.acos(Math.sin(declinacion)*Math.sin((Math.PI/180)*(latitud)) + Math.cos(declinacion)*Math.cos((Math.PI/180)*(latitud))*Math.cos(h))*100)/100);
        }
        return cenital;
    }

    get cenital(){
        return this.cenital;
    }
}
const Gsc = 1367;

class RadiacionSolar{
    
    static get Gsc(){
        return this.Gsc;
    }

    constructor(dia_n, cenital, concentracion, transmitancia, altura, tipo_clima){
        this.radiacion_extraterrestre = this.calcular_radiacion_extraterrestre(
            this.__Gsc,
            dia_n
        );
        this.a0 = this.calcular_a0(
            tipo_clima.r0,
            altura
        );       
        this.a1 = this.calcular_a1(
            tipo_clima.r1,
            altura
        );
        this.k = this.calcular_k(
            tipo_clima.rk,
            altura
        );
        this.tb = this.calcular_tb(
            this.a0,
            this.a1,
            this.k,
            cenital
        );
        this.radiacion_DNI = this.calcular_DNI(
            this.tb,
            this.radiacion_extraterrestre
        );
        this.radiacion_incidente = this.calcular_radiacion_incidente(
            concentracion,
            transmitancia,
            this.radiacion_DNI
        );
        this.promedio_diario_DNI = this.calcular_promedio(
            this.radiacion_DNI
        );
        this.promedio_diario_incidente = this.calcular_promedio(
            this.radiacion_incidente
        );
    }
        
    calcular_radiacion_extraterrestre(Gsc, dia_n){
        var radiacion_solar = Gsc*(1+Math.cos(2*Math.PI*dia_n/365)/30);
        return radiacion_solar;
    }

    get radiacion_extraterrestre(){
        return this.radiacion_extraterrestre;
    }

    calcular_a0(r0, altura){
        var a0 = (0.4237-0.00821*((6-altura)**2))*r0;
        return a0;
    }

    get a0(){
        return this.a0;
    }

    calcular_a1(r1, altura){
        var a1 = (0.5055+0.00595*((6.5-altura)**2))*r1;
        return a1;
    }

    get a1(){
        return this.a1;
    }

    calcular_k(rk, altura){
        var k = (0.2711+0.01858**((2.5-altura)**2))*rk;
        return k;
    }

    get k(){
        return this.k;
    }
    
    calcular_tb(a0, a1, k, cenit){
        var tb = [];
        var c = 0;
        for(c=0;c < cenit.length;c++){
            tb.push(Math.round((a0+a1*(Math.exp(Math.round(-k/Math.cos(cenit[c])*100)/100)))*100)/100);
        }
        return tb;
    }

    get tb(){
        return this.tb;
    }

    calcular_DNI(tb, radiacion_extraterrestre){
        var DNI = [];
        var t = 0;
        for(t=0;t < tb.length;t++){
            DNI.push(Math.round(t*radiacion_extraterrestre*100)/100);
        }
        return DNI;
    }

    get DNI(){
        return this.DNI;
    }
    
    calcular_promedio(valor){
        var promedio = 0;
        var d = 0;
        for(d=0;d < valor.length;d++){
            promedio = promedio + valor[d];
        }
        promedio = promedio/valor.length;
        return promedio;
    }

    get promedio(){
        return this.promedio;
    }

    calcular_radiacion_incidente(concentracion, transmitancia, radiacion_directa){
        incidente = [];
        r = 0;
        for(r=0;r < radiacion_directa.length; r++){
            incidente.push(concentracion*transmitancia*radiacion_directa[r]);
        }
        return incidente;
    }

    get radiacion_incidente(){
        return this.radiacion_incidente;
    }
}

const boltzman = 5.67*10**-8;

class Calculo{
    
    static get boltzman(){
        return boltzman;
    }

    constructor(radiacion_solar, li_temp, ls_temp, area, emisividad){
        this.temperaturas_receptor = this.generar_aleatorios(
            radiacion_solar.radiacion_incidente.length, 
            li_temp, 
            ls_temp
        );
        this.radiacion_solar = radiacion_solar
        this.potencia_rad = this.calcular_potencia_radiante(
            area, 
            emisividad, 
            this.temperaturas_receptor, 
            this.__boltzman
        );
    }

    generar_aleatorios(cantidad, limite_inferior, limite_superior){
        var aleatorios = [];
        var i = 0;
        for(i=0;i < cantidad; i++){
            aleatorios.push(Math.round(Math.random()*(limite_superior-limite_inferior)*100)/100 + limite_inferior)
        }
        aleatorios.sort();
        return aleatorios;
    }

    get temperatura_receptor(){
        return this.temperaturas_receptor;
    }

    calcular_potencia_radiante(area, emisividad, temperatura_receptor, boltzman){
        var potencia_rad = [];
        var t = 0;
        for(t=0;t < temperatura_receptor;t++){
            c = area*emisividad*boltzman*((temperatura_receptor[c]+273)**4);
            potencia_rad.push(c);
        }
        return potencia_rad;
    }

    get potencia_rad(){
        return this.potencia_rad;
    }
}