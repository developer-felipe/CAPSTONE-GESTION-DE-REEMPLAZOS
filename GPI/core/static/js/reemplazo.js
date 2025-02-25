
document.addEventListener('DOMContentLoaded', function () {
    const boton = document.querySelectorAll(".btn-edit");

    boton.forEach(function (boton) {
        boton.addEventListener("click", function () {
            const idReemplazo = boton.id.split('-')[2];
            const ids = boton.id.split('-').slice(2);
            const semana = boton.dataset.semana;
            const profesor = boton.dataset.profesor;
            const asignatura = boton.dataset.asignatura;
            const seccion = boton.dataset.seccion;
            const sala = boton.dataset.sala;
            const modulo = boton.dataset.modulo;
            const num_ = boton.dataset.num_modulo;
            const dia = boton.dataset.dia;
            const fecha = boton.dataset.fecha;
            const profesor_remp = boton.dataset.profesor_remp;
            const id_modulo = document.getElementById("reg_mod").dataset.remp_id;
            const id_dia = document.getElementById("reg_dia").dataset.dia_id;
            const id_modulos = id_modulo.split('-');
            const tbody = document.getElementById('body-edit');
            tbody.innerHTML = '';

            ids.forEach((id, index) => {
                const tr = document.createElement('tr');
                const reemplazoId = idReemplazo[index];
                tr.setAttribute('data-reemplazoId', reemplazoId);

                tr.innerHTML = `
                    <td>
                        <select class="form-select" name="edit_semana" required>
                            <option value="">N° Semana</option>
                            ${[...Array(18).keys()].map(i => {
                    return `<option value="${i + 1}" ${semana == i + 1 ? 'selected' : ''}>Semana ${i + 1}</option>`;
                }).join('')}
                        </select>
                    </td>
                    <td>${profesor}</td>
                    <td>${asignatura}</td>
                    <td>${seccion}</td>
                    <td>${sala}</td>
                    <td class="modulo">...</td>
                    <td>${dia}</td>
                    <td>${fecha}</td>
                    <td>
                        <select class="form-select" name="profesor_remp" required>
                            <option value="">Seleccionar profesor</option>
                        </select>
                    </td>
                `;
                tbody.appendChild(tr);

                const moduloId = id_modulos[index];
                if (moduloId && moduloId !== 'undefined') {
                    fetch(`/modulo_por_id/${moduloId}`)
                        .then(response => response.json())
                        .then(data => {
                            const moduloTd = tr.querySelector('td.modulo');
                            if (data) {
                                moduloTd.textContent = data.hora_modulo;
                            } else {
                                moduloTd.textContent = 'Módulo no encontrado';
                            }
                        })
                        .catch(error => {
                            console.error('Error al obtener el módulo:', error);
                            const moduloTd = tr.querySelector('td.modulo');
                            moduloTd.textContent = 'Error al cargar módulo';
                        });
                } else {
                    console.error('Error: El ID del módulo es inválido.');
                }
                fetch(`/reemplazos/profesor_por_nombre/${encodeURIComponent(profesor_remp)}`)
                    .then(response => response.json())
                    .then(data => {
                        let profesorId = null;
                        if (data.profesores && data.profesores.length > 0) {
                            const profesorEncontrado = data.profesores[0];
                            profesorId = profesorEncontrado.id_profesor;
                        }
                        fetch(`/obtener_profesores_disponibles/?dia_semana=${id_dia}&modulo_id=${moduloId}`)
                            .then(response => response.json())
                            .then(data => {
                                const selectReemplazo = tr.querySelector('td select[name="profesor_remp"]');
                                selectReemplazo.innerHTML = '';
                                if (data.profesores && data.profesores.length > 0) {
                                    const defaultOption = document.createElement('option');
                                    defaultOption.textContent = 'Seleccione un profesor';
                                    defaultOption.disabled = true;
                                    defaultOption.selected = true;
                                    selectReemplazo.appendChild(defaultOption);
                                    data.profesores.forEach(profesor => {
                                        const option = document.createElement('option');
                                        option.value = profesor.id_profesor;
                                        option.textContent = `${profesor.nombre} ${profesor.segundo_nombre || ''} ${profesor.apellido} ${profesor.segundo_apellido || ''}`.trim();
                                        if (profesor.id_profesor == profesorId) {
                                            option.selected = true;
                                        }
                                        selectReemplazo.appendChild(option);
                                    });
                                } else {
                                    const option = document.createElement('option');
                                    option.textContent = 'No hay profesores disponibles para este módulo';
                                    option.disabled = true;
                                    selectReemplazo.appendChild(option);
                                }
                            })
                            .catch(error => {
                                console.error('Error al obtener los profesores para el módulo:', error);
                            });
                    })
                    .catch(error => {
                        console.error('Hubo un problema con la solicitud Fetch de profesor:', error);
                    });
            });
        });
    });

    fetch('/profesores_con_licencia_no_asignada/')
        .then(response => response.json())
        .then(data => {
            const docentesSelect = document.getElementById('docente');
            docentesSelect.innerHTML = '<option value="">Selecciona un docente con licencia</option>';
            const profesores = data.profesores;

            if (profesores.length > 0) {
                profesores.forEach(profesor => {
                    let nombreCompleto = `${profesor.nombre} ${profesor.apellido}`;
                    if (profesor.segundo_nombre) {
                        nombreCompleto = `${profesor.nombre} ${profesor.segundo_nombre} ${profesor.apellido}`;
                    }
                    if (profesor.segundo_apellido) {
                        nombreCompleto = `${profesor.nombre} ${profesor.segundo_nombre || ''} ${profesor.apellido} ${profesor.segundo_apellido}`;
                    }
                    const option = document.createElement('option');
                    option.value = profesor.id_profesor;
                    option.textContent = nombreCompleto.trim();
                    option.setAttribute('data-bs-id-licencia', profesor.id_licencia);
                    option.setAttribute('data-bs-fecha-inicio', profesor.fecha_inicio);
                    option.setAttribute('data-bs-fecha-termino', profesor.fecha_termino);
                    docentesSelect.appendChild(option);
                });
            } else {
                const option = document.createElement('option');
                option.value = '';
                option.textContent = 'No hay docentes con licencias no asignadas.';
                docentesSelect.appendChild(option);
            }
        })
        .catch(error => {
            console.error('Error al obtener los docentes:', error);
        });
});


const actualizar = document.getElementById('actualizar');
actualizar.addEventListener('click', function () {
    const tbody = document.getElementById('body-edit');
    const filas = tbody.querySelectorAll('tr');

    filas.forEach(function (fila) {
        const reemplazoId = fila.getAttribute('data-reemplazoId');
        console.log('Reemplazo ID:', reemplazoId);
        const semanaSelect = fila.querySelector('select[name="edit_semana"]');
        const profesorSelect = fila.querySelector('select[name="profesor_remp"]');
        const semanaValue = semanaSelect.value;
        const profesorOption = profesorSelect.options[profesorSelect.selectedIndex];
        const profesorValue = profesorOption.textContent.trim();

        console.log('Semana:', semanaValue, 'Profesor:', profesorValue);

        if (semanaValue && profesorValue) {
            fetch('/reemplazos/actualizar_reemplazo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },

                body: JSON.stringify({
                    semana: semanaValue,
                    profesor_remp: profesorValue,
                    reemplazoId: reemplazoId,
                }),
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        console.log('Reemplazo actualizado');
                        location.reload();
                    } else {
                        console.error('Error al actualizar el reemplazo');
                    }
                })
                .catch(error => {
                    console.error('Error al hacer la solicitud de actualización:', error);
                });
        }
    });
});

document.getElementById('envio').addEventListener('click', function (e) {
    e.preventDefault();
    const formulario = document.querySelector('form');
    const reemplazosData = [];
    const rows = document.querySelectorAll('#tabla-clases tbody tr');
    const selectedOption = document.querySelector('option:checked');
    const idLicencia = selectedOption ? selectedOption.getAttribute('data-bs-id-licencia') : null;

    if (!idLicencia) {
        console.error('No se ha seleccionado una opción válida para id_licencia');
        alert('Por favor, selecciona una opción de licencia.');
        return;
    }
    rows.forEach(row => {
        const semanaSelect = row.querySelector('select[name^="semana_"]');
        const profesorSelect = row.querySelector('select[name="profesor_reemplazo"]');
        const selectedOption = profesorSelect.options[profesorSelect.selectedIndex];
        const profesor_reemplazo = selectedOption ? selectedOption.textContent.trim() : null;
        const profesor_reemplazo_select = profesorSelect ? profesorSelect.value : null;
        let tdAsignatura = row.querySelector('td[data-bs-id-asignatura]');
        let idAsignatura = tdAsignatura.dataset.bsIdAsignatura;
        const semana = semanaSelect ? semanaSelect.value : null;
        const fecha_clase = row.querySelector('td:nth-child(7)').textContent.trim();
        const asignatura = row.querySelector('td:nth-child(2)').textContent.trim();
        const [day, month, year] = fecha_clase.split('-');
        const fechaFormateada = `${year}-${month}-${day}`;
        const reemplazado = profesor_reemplazo_select !== 'n/a';
        if (semana && profesor_reemplazo && profesor_reemplazo_select) {
            reemplazosData.push({
                semana,
                fecha_reemplazo: fechaFormateada,
                profesor_reemplazo,
                horario_id: idAsignatura,
                asignatura,
                reemplazado
            });
        }
        console.log(reemplazosData)
    });
    if (reemplazosData.length > 0) {
        fetch('/registrar_reemplazo/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                reemplazos: reemplazosData,
                id_licencia: idLicencia
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert('Reemplazos registrados con éxito.');
                    location.reload();
                } else {
                    alert('Hubo un error al registrar los reemplazos.');
                }
            })
            .catch(error => {
                console.error('Error al enviar los reemplazos:', error);
            });
    } else {
        alert('Por favor, selecciona todos los campos necesarios.');
    }
});

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

document.getElementById('docente').addEventListener('change', function () {
    const docenteId = this.value;
    const selectedOption = this.options[this.selectedIndex];
    const fechaInicio = selectedOption.getAttribute('data-bs-fecha-inicio');
    const fechaTermino = selectedOption.getAttribute('data-bs-fecha-termino');

    if (docenteId && fechaInicio && fechaTermino) {
        const url = `/obtener_clases_por_docente/?docente_id=${encodeURIComponent(docenteId)}&fecha_inicio=${encodeURIComponent(fechaInicio)}&fecha_termino=${encodeURIComponent(fechaTermino)}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                const clases = data.clases || []
                const tablaClases = document.getElementById('tabla-clases').getElementsByTagName('tbody')[0];
                tablaClases.innerHTML = '';
                if (clases.length === 0) {
                    tablaClases.innerHTML = `<tr><td colspan="8" class="text-center">No hay clases programadas para este docente durante el rango de fechas.</td></tr>`;
                } else {
                    clases.forEach(clase => {
                        const row = tablaClases.insertRow();
                        row.innerHTML = `
                        <td><select class="form-select" name="semana_${clase.id}" required>
                        <option value="">N° Semana</option>${[...Array(18).keys()].map(i => `<option value="${i + 1}">Semana ${i + 1}</option>`).join('')}
                        </select></td>
                        <td data-bs-id-asignatura="${clase.id_horario}">${clase.asignatura}</td>
                        <td>${clase.seccion}</td>
                        <td>${clase.sala}</td>
                        <td>${clase.modulo}</td>
                        <td>${clase.dia}</td>
                        <td>${clase.fecha_clase}</td>
                        <td><select id="profesor_reemplazo_${clase.id_horario}" name="profesor_reemplazo" class="form-select" required>
                        <option value="">Selecciona un profesor reemplazante</option>
                        <option value="n/a">ASIGNAR CLASE A RECUPERACIÓN</option></select></td>`;
                        
                        const selectReemplazo = row.querySelector(`#profesor_reemplazo_${clase.id_horario}`);
                        fetch(`/obtener_profesores_disponibles/?dia_semana=${clase.dia_semana_id}&modulo_id=${clase.modulo_id}`)
                            .then(response => response.json())
                            .then(data => {

                                if (data.profesores && data.profesores.length > 0) {
                                    data.profesores.forEach(profesor => {
                                        const option = document.createElement('option');
                                        option.value = profesor.id_profesor;
                                        option.textContent = `${profesor.nombre} ${profesor.segundo_nombre || ''} ${profesor.apellido} ${profesor.segundo_apellido || ''}`.trim();
                                        selectReemplazo.appendChild(option);
                                    });
                                    const recuperacionOption = document.createElement('option');
                                    recuperacionOption.value = 'n/a';
                                    recuperacionOption.textContent = 'ASIGNAR CLASE A RECUPERACIÓN';
                                    selectReemplazo.appendChild(recuperacionOption);
                                }
                            })
                            .catch(error => {
                                console.error('Error al obtener los profesores:', error);
                            });
                    });
                }
            })
            .catch(error => {
                console.error('Error al obtener las clases:', error);
            });
    } else {
        console.error('Faltan parámetros: docenteId, fechaInicio o fechaTermino');
    }
});