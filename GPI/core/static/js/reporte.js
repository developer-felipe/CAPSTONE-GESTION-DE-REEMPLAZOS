function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
const csrftoken = getCookie("csrftoken");

async function enviarDatos() {
  const fechaInicio = document.getElementById("fechaInicio").value;
  const fechaTermino = document.getElementById("fechaFin").value;
  const profesorId = document.getElementById("docente").value;

  if (fechaInicio && fechaTermino && profesorId) {
    console.log("Fecha Inicio:", fechaInicio);
    console.log("Fecha Término:", fechaTermino);
    console.log("ID Profesor:", profesorId);

    const url = `/horas_periodo/?fechaInicio=${fechaInicio}&fechaTermino=${fechaTermino}&profesorId=${profesorId}`;

    try {
      const response = await fetch(url, {
        method: "GET",
        headers: {
          "X-CSRFToken": csrftoken,
        },
      });

      if (!response.ok) {
        throw new Error(`Error al enviar datos: ${response.statusText}`);
      }

      const result = await response.json();
      console.log("Respuesta del servidor:", result);

      const reemplazos = result.reemplazos;
      const horas_horarios = result.horas_horarios;
      const horas_reemplazo = result.horas_reemplazo;
      const total_horas = result.horas_totales;
      const tipo_pago = result.tipo_pago;

      const reportSection = document.querySelector(".report-section");

      const tableHTML = `
          <h3 class="text-center">Reporte</h3>
          <div class="table-responsive">
              <table class="table table-striped table-hover table-bordered text-center">
                  <thead class="thead-dark">
                      <tr>
                          <th>Semana</th>
                          <th>Sección</th>
                          <th>Jornada</th>
                          <th>Hora</th>
                          <th>Nro de módulos</th>
                          <th>Sala</th>
                          <th>Fecha</th>
                          <th>Profesor</th>
                          <th>Profesor Reemplazante</th>
                      </tr>
                  </thead>
                  <tbody id="reportBody">
                      ${
                        reemplazos.length === 0
                          ? `<tr><td colspan="9">No se encontraron reportes para el docente y en el periodo seleccionado.</td></tr>`
                          : reemplazos
                              .map((reemplazo) => {
                                return `
                                <tr>
                                    <td>${reemplazo.semana}</td>
                                    <td>${reemplazo.seccion}</td>
                                    <td>${reemplazo.nombre_asignatura}</td>
                                    <td>${reemplazo.hora_modulo}</td>
                                    <td>${reemplazo.registros}</td>
                                    <td>${reemplazo.numero_sala}</td>
                                    <td>${reemplazo.fecha_reemplazo}</td>
                                    <td>${reemplazo.profesor_nombre}</td>
                                    <td>${reemplazo.profesor_reemplazo}</td>
                                </tr>
                              `;
                              })
                              .join("")
                      }
                      <tr class="font-weight-bold">
                      </tr>
                      <tr>
                          <td colspan="8" class="font-weight-bold">Horas totales por Horario:</td>
                          <td>${horas_horarios}</td>
                      </tr>
                      <tr>
                          <td colspan="8" class="font-weight-bold">Horas totales de Reemplazo:</td>
                          <td>${horas_reemplazo}</td>
                      </tr>
                      <tr>
                          <td colspan="8" class="font-weight-bold">Horas totales de Reemplazo:</td>
                          <td>${total_horas}</td>
                      </tr>
                      <tr>
                          <td colspan="8" class="font-weight-bold">Tipo de pago:</td>
                          <td>${tipo_pago}</td>
                      </tr>
                  </tbody>
              </table>
          </div>
          <div class="text-center mt-4">
              <button class="btn btn-dark" onclick="emitirInforme()">Emitir Informe</button>
          </div>`;

      reportSection.innerHTML = tableHTML;
    } catch (error) {
      console.error("Error al enviar los datos:", error);
    }
  } else {
    console.log(
      "Faltan datos: asegúrate de que todos los campos estén completos."
    );
  }
}
