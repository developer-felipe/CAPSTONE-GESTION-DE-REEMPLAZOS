let horariosAsignados = [];
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

function checkOption(select, modalId) {
    if (select.value === 'agregar') {
        $(`#${modalId}`).modal('show');
    }
}

document.querySelectorAll('.modal.fade').forEach(modal => {
    modal.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
        }
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('form');
    if (form) {
        const profesorID = form.dataset.prof_id;
        fetch(`/obtener_horarios/${profesorID}/`)
            .then(response => response.json())
            .then(data => {
                if (data.horarios && data.horarios.length > 0) {
                    cargarHorariosEnDOM(data.horarios);
                } else {
                    console.log('No se encontraron horarios para este profesor');
                }
            })
            .catch(error => console.error('Error al obtener los horarios:', error));
    } else {
        console.error('Formulario con ID "form" no encontrado');
    }
});
function cargarHorariosEnDOM(horarios) {
    horarios.forEach(horario => {
        const celda = document.querySelector(`#div-horario table tbody tr:nth-child(${parseInt(horario.id_modulo)}) td:nth-child(${parseInt(horario.id_dia) + 1})`);
        const arraypos = horariosAsignados.length
        if (celda) {
            celda.innerHTML = `
            <div class="d-flex flex-column p-2 bg-light border rounded shadow-sm position-relative text-center">
                <button type="button" class="btn btn-danger btn-sm position-absolute top-0 end-0 m-1" 
                        onclick="desasignarBloque(${horario.id_modulo}, ${horario.id_dia}, ${arraypos})">
                    <span class="material-icons" style="font-size: 16px;">close</span>
                </button>
                <div class="mb-2">
                    <span class="text-primary font-weight-bold">${horario.asignatura} (${horario.jornada})</span>
                </div>
                <div class="small text-muted">Sección: ${horario.seccion}</div>
                <div class="small text-muted">Sala: ${horario.sala}</div>
            </div>
        `;
            horariosAsignados.push({
                array_pos: arraypos,
                asignaturaID: horario.id_asignatura,
                diaID: horario.id_dia,
                jornada: horario.jornada,
                moduloID: horario.id_modulo,
                salaID: horario.id_sala,
                seccion: horario.seccion,
                carreraID: horario.id_carrera,
            });
            console.log('DOM TRAE:', horariosAsignados)
        } else {
            console.log(`No se encontró la celda para el día ${horario.dia} y módulo ${horario.modulo}`);
        }
    });
}



function actualizarBloque(moduloID, diaID, asignatura, jornada, sala, seccion, array_pos) {
    const celda = document.querySelector(`#div-horario table tbody tr:nth-child(${parseInt(moduloID)}) td:nth-child(${parseInt(diaID) + 1})`);
    if (celda) {
        celda.innerHTML = `
            <div class="d-flex flex-column p-2 bg-light border rounded shadow-sm position-relative text-center">
                <button type="button" class="btn btn-danger btn-sm position-absolute top-0 end-0 m-1" 
                        onclick="desasignarBloque(${moduloID}, ${diaID}, ${array_pos})">
                    <span class="material-icons" style="font-size: 16px;">close</span>
                </button>
                <div class="mb-2">
                    <span class="text-primary font-weight-bold">${asignatura}(${jornada})</span>
                </div>
                <div class="small text-muted">Sección: ${seccion}</div>
                <div class="small text-muted">Sala: ${sala}</div>
            </div>
        `;
    }
}

function desasignarBloque(moduloID, diaID, array_pos) {
    console.log(array_pos)
    const celda = document.querySelector(`#div-horario table tbody tr:nth-child(${parseInt(moduloID)}) td:nth-child(${parseInt(diaID) + 1})`);
    if (celda) {
        celda.innerHTML = `
            <div class="d-flex align-items-center justify-content-center">
                <button type="button" class="btn btn-warning" data-bs-toggle="modal" data-bs-target="#asignar"
                    data-modulo-id="${moduloID}" data-dia-id="${diaID}" onclick="obtenerDiaModulo(this)">
                    <span class="material-icons me-2" style="font-size: 16px;">add</span>
                </button>
            </div>
        `;
        celda.style.backgroundColor = "";
        horariosAsignados.splice(array_pos, 1)
        console.log(horariosAsignados)
    }
}

$(document).ready(function () {
    const profesorID = form.dataset.prof_id;
    console.log(profesorID);

    $('#btn-horario').on('click', function () {
        const primerNombre = $('#primer_nombre').val().trim();
        const primerApellido = $('#primer_apellido').val().trim();

        if (primerNombre === '' || primerApellido === '') {
            alert('El primer nombre y el primer apellido son obligatorios.');
            return;
        }

        const datosFormulario = {
            profesor: {
                id: profesorID,
                nombre: primerNombre.toUpperCase(),
                apellido: primerApellido.toUpperCase(),
                segundo_nombre: $('#segundo_nombre').val().toUpperCase() || '',
                segundo_apellido: $('#segundo_apellido').val().toUpperCase() || ''
            },
            horarios_asignados: horariosAsignados
        };

        console.log("Enviando:", datosFormulario);

        fetch('/editar_profesor/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify(datosFormulario)
        })
            .then(response => response.json())
            .then(data => {
                alert('Profesor y horarios actualizados exitosamente!');
                console.log(data);
                window.location.href = '{% url "docente" %}';
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Hubo un error al editar el profesor y los horarios.');
            });
    });
});

async function obtenerSalas() {
    try {
        const response = await fetch('/salas/');
        const data = await response.json();
        const select = $('#sala');
        select.empty();
        select.append('<option value="">Selecciona una sala</option>');
        data.forEach(function (sala) {
            select.append(`<option value="${sala.id_sala}">${sala.numero_sala}</option>`);
        });
        select.append('<option value="agregar">Agregar sala</option>');
    } catch (error) {
        console.log('Error al obtener salas:', error);
    }
}

async function obtenerAsignaturas() {
    try {
        const response = await fetch('/asignaturas/');
        const data = await response.json();
        const select = $('#asignatura');
        select.empty();
        select.append('<option value="">Selecciona una asignatura</option>');
        data.forEach(function (asignatura) {
            select.append(`<option value="${asignatura.id_asignatura}">${asignatura.nombre_asignatura}</option>`);
        });
        select.append('<option value="agregar">Agregar asignatura</option>');
    } catch (error) {
        console.log('Error al obtener asignaturas:', error);
    }
}

async function obtenerCarreras() {
    try {
        const response = await fetch('/carreras/', {
            method: 'GET',
            headers: {
                "X-CSRFToken": csrftoken,
            },
        });
        if (!response.ok) {
            throw new Error(`Error al recibir datos: ${response.statusText}`);
        }
        const data = await response.json();
        const select = $('#carrera');
        select.empty();
        select.append('<option value="">Selecciona una carrera</option>');

        data.forEach(function (carrera) {
            select.append(`<option value="${carrera.id_carrera}">${carrera.nombre_carrera}</option>`);
        });
        select.append('<option value="agregar">Agregar carrera</option>');
    } catch (error) {
        console.error('Error al obtener carreras:', error);
    }
}

$(document).ready(function () {
    obtenerAsignaturas();
    obtenerSalas();
    obtenerCarreras()
});

document.getElementById('btn-bloque').addEventListener('click', function () {
    const moduloID = this.getAttribute('data-modulo-id');
    const diaID = this.getAttribute('data-dia-id');
    const asignaturaSelect = document.getElementById('asignatura');
    const asignaturaID = asignaturaSelect.value;
    const asignaturaTexto = asignaturaSelect.options[asignaturaSelect.selectedIndex].text
    const jornadaSelect = document.getElementById('jornada').value;
    const seccionSelect = document.getElementById('seccion').value;
    const salaSelect = document.getElementById('sala');
    const salaID = salaSelect.value;
    const salaTexto = salaSelect.options[salaSelect.selectedIndex].text
    const carreraSelect = document.getElementById('carrera');
    const carreraID = carreraSelect.value;
    if (asignaturaID && jornadaSelect && seccionSelect && salaID) {
        const array_pos = horariosAsignados.length
        horariosAsignados.push({
            moduloID: moduloID,
            diaID: diaID,
            asignaturaID: asignaturaID,
            jornada: jornadaSelect,
            seccion: seccionSelect,
            salaID: salaID,
            carreraID: carreraID,
            array_pos: array_pos
        });
        actualizarBloque(moduloID, diaID, asignaturaTexto, jornadaSelect, salaTexto, seccionSelect, array_pos);
        $('#asignar').modal('hide');
        console.log(horariosAsignados)
    } else {
        alert('Por favor, completa todos los campos.');
    }
});

function addCarrera() {
    const nuevaCarrera = document.getElementById('nueva-carrera').value.trim();
    if (nuevaCarrera === '') {
        alert('Por favor, ingrese un nombre válido para la carrera');
        return;
    }
    const carreraCapitalizada = nuevaCarrera.toUpperCase();
    fetch('/carreras/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ nombre: carreraCapitalizada })
    })
        .then(response => response.json())
        .then(data => {
            const newOption = new Option(carreraCapitalizada, data.id);
            console.log(newOption);
            const select = document.getElementById('carrera');
            const options = select.children;
            if (options.length > 1) {
                select.insertBefore(newOption, options[options.length - 1]);
            } else {
                select.appendChild(newOption);
            }
            document.getElementById('nueva-carrera').value = '';
            select.value = data.id;
            $('#agregarCarrera').modal('hide');
        })
        .catch(error => {
            console.log('Error al agregar carrera:', error);
            alert('Hubo un error al agregar la carrera.');
        });
}

function addAsignatura() {
    const nuevaAsignatura = document.getElementById('nueva-asignatura').value.trim();
    if (nuevaAsignatura === '') {
        alert('Por favor, ingrese un nombre válido para la asignatura');
        return;
    }
    const asignaturaCapitalizada = nuevaAsignatura.toUpperCase();
    fetch('/asignaturas/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ nombre: asignaturaCapitalizada })
    })
        .then(response => response.json())
        .then(data => {
            const newOption = new Option(asignaturaCapitalizada, data.id);
            console.log(newOption)
            const select = document.getElementById('asignatura');
            const options = select.children;
            if (options.length > 1) {
                select.insertBefore(newOption, options[options.length - 1]);
            } else {
                select.appendChild(newOption);
            }
            document.getElementById('nueva-asignatura').value = '';
            select.value = data.id;
            $('#agregarAsignatura').modal('hide');
        })
        .catch(error => {
            console.log('Error al agregar asignatura:', error);
            alert('Hubo un error al agregar la asignatura.');
        });
}

function addAsignatura() {
    const nuevaAsignatura = document.getElementById('nueva-asignatura').value.trim();
    if (nuevaAsignatura === '') {
        alert('Por favor, ingrese un nombre válido para la asignatura');
        return;
    }
    const asignaturaCapitalizada = nuevaAsignatura.toUpperCase();
    fetch('/asignaturas/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ nombre: asignaturaCapitalizada })
    })
        .then(response => response.json())
        .then(data => {
            const newOption = new Option(asignaturaCapitalizada, data.id);
            console.log(newOption)
            const select = document.getElementById('asignatura');
            const options = select.children;
            if (options.length > 1) {
                select.insertBefore(newOption, options[options.length - 1]);
            } else {
                select.appendChild(newOption);
            }
            document.getElementById('nueva-asignatura').value = '';
            select.value = data.id;
            $('#agregarAsignatura').modal('hide');
        })
        .catch(error => {
            console.log('Error al agregar asignatura:', error);
            alert('Hubo un error al agregar la asignatura.');
        });
}


function addSala() {
    let nuevaSala = document.getElementById('nueva-sala').value.trim();

    if (nuevaSala === '') {
        alert('Por favor, ingrese un nombre para la sala.');
        return;
    }
    if (nuevaSala.length !== 4) {
        alert('El nombre de la sala debe tener exactamente 4 caracteres.');
        return;
    }
    nuevaSala = nuevaSala.toUpperCase();

    fetch('/salas/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ numero_sala: nuevaSala })
    })
        .then(response => response.json())
        .then(data => {
            const newOption = new Option(nuevaSala, data.id);
            newOption.value = data.id_sala;

            const select = document.getElementById('sala');
            const options = select.children;
            if (options.length > 1) {
                select.insertBefore(newOption, options[options.length - 1]);
            } else {
                select.appendChild(newOption);
            }

            document.getElementById('nueva-sala').value = '';
            $('#agregarSalaModal').modal('hide');
        })
        .catch(error => {
            console.log('Error al agregar sala:', error);
            alert('Hubo un error al agregar la sala.');
        });
}

document.getElementById('seccion').addEventListener('blur', function () {
    let value = this.value;
    if (!isNaN(value) && value !== '') {
        let numValue = parseInt(value);
        if (numValue > 999) {
            this.value = '';
        } else {
            let formattedValue = String(numValue).padStart(3, '0');
            this.value = formattedValue;
        }
    }
});

function obtenerDiaModulo(button) {
    const moduloID = button.getAttribute('data-modulo-id');
    const diaID = button.getAttribute('data-dia-id');
    document.getElementById('btn-bloque').setAttribute('data-modulo-id', moduloID);
    document.getElementById('btn-bloque').setAttribute('data-dia-id', diaID);
}
