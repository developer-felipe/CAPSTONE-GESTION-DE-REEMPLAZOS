$(document).ready(function () {
     $('#editModal').on('show.bs.modal', function (event) {
         const button = $(event.relatedTarget);  
         const id = button.data('id');
         const profesorNombreCompleto = button.data('profesor'); 
         const asignaturaNombre = button.data('asignatura'); 
         const salaNombre = button.data('sala'); 
         const numeroModulos = button.data('numero_modulos');
         const fechaClase = button.data('fecha_clase');
         const fechaRecuperacion = button.data('fecha_recuperacion');
         const horaRecuperacion = button.data('hora_recuperacion');
 
         $('#edit_id').val(id);
         $('#edit_numero_modulos').val(numeroModulos);
         $('#edit_fecha_clase').val(fechaClase);
         $('#edit_fecha_recuperacion').val(fechaRecuperacion);
         $('#edit_hora_recuperacion').val(horaRecuperacion);
 
         fetch('/docente_recuperación/')
             .then(response => response.json())
             .then(data => {
                 const profesorSelect = $('#edit_profesor');
                 profesorSelect.empty(); 
                 let profesorEncontrado = false; 
 
                 data.profesores.forEach(profesor => {
                     const nombreCompleto = `${profesor.nombre} ${profesor.segundo_nombre || ''} ${profesor.apellido} ${profesor.segundo_apellido || ''}`.trim();
 
                     if (nombreCompleto === profesorNombreCompleto) {
                         profesorEncontrado = true;
                     }
 
                     profesorSelect.append(
                         `<option value="${profesor.id_profesor}" ${nombreCompleto === profesorNombreCompleto ? 'selected' : ''}>
                             ${nombreCompleto}
                         </option>`
                     );
                 });
 
                 if (!profesorEncontrado) {
                     profesorSelect.append(
                         `<option value="" disabled selected>Profesor no disponible</option>`
                     );
                 }
 
                 profesorSelect.val(profesorSelect.find('option:selected').val()).change(); 
             })
             .catch(error => console.error('Error al cargar los profesores:', error));
 
         fetch('/todas_asignaturas/')  
             .then(response => response.json())
             .then(data => {
                 const asignaturaSelect = $('#edit_asignatura');
                 asignaturaSelect.empty(); 
                 data.todas_asignaturas.forEach(asignatura => {
                     asignaturaSelect.append(
                         `<option value="${asignatura.id_asignatura}" ${asignatura.nombre_asignatura === asignaturaNombre ? 'selected' : ''}>
                             ${asignatura.nombre_asignatura}
                         </option>`
                     );
                 });
                 asignaturaSelect.val(asignaturaSelect.find('option:selected').val()).change(); 
             })
             .catch(error => console.error('Error al cargar las asignaturas:', error));
 
         fetch('/salas/')
             .then(response => response.json())
             .then(data => {
                 const salaSelect = $('#edit_sala');
                 salaSelect.empty();
                 data.forEach(sala => {
                     salaSelect.append(
                         `<option value="${sala.id_sala}" ${sala.numero_sala === salaNombre ? 'selected' : ''}>
                             ${sala.numero_sala}
                         </option>`
                     );
                 });
                 salaSelect.val(salaSelect.find('option:selected').val()).change(); 
             })
             .catch(error => console.error('Error al cargar las salas:', error));
     });
 });
 