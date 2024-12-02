document.addEventListener("DOMContentLoaded", function () {
  const formReemplazo = document.getElementById("formReemplazo");
  formReemplazo.addEventListener("click", function () {
    console.log("click en formReemplazo");
    fetch("/profesores/")
      .then((response) => response.json())
      .then((profesores) => {
        const divSelection = document.querySelector("#reporte_reemplazo");
        let opcionesDocentes =
          '<option value="">Seleccione un docente</option>';

        profesores.forEach((profesor) => {
          opcionesDocentes += `<option value="${profesor.id}">${profesor.nombre_completo}</option>`;
        });

        divSelection.innerHTML = `
          <div class="card mb-3 mx-auto w-50 mt-5">
              <div class="card-body">
                  <h3 class="text-center">Filtro para Informe de Reemplazos</h3>
                  <form method="GET" action="{% url 'reportes' %}">
                      <div class="form-group">
                          <div class="mb-3">
                              <label for="docente">Nombre docente:</label>
                              <select id="docente" name="docente" class="form-control" required>
                                  ${opcionesDocentes}
                              </select>
                          </div>
                      </div>
                      <div class="form-group">
                          <div class="mb-3">
                              <label for="fechaInicio" class="form-label">Fecha de Inicio</label>
                              <input type="date" class="form-control" id="fechaInicio" name="fecha_inicio" required>
                          </div>
                          <div class="mb-3">
                              <label for="fechaFin" class="form-label">Fecha de Término</label>
                              <input type="date" class="form-control" id="fechaFin" name="fecha_fin" required>
                          </div>
                      </div>
                      <div class="text-center">
                          <button id="btn-filtro-reemplazo" type="button" class="btn btn-success btn-block mt-3" onclick="enviarDatos()">Buscar</button>
                      </div>
                  </form>
              </div>
          </div>
        `;
        document.getElementById("reporte_dara").innerHTML = "";
      })
      .catch((error) =>
        console.error("Error al cargar los profesores:", error)
      );
  });

  const formDARA = document.getElementById("formDARA");
  formDARA.addEventListener("click", function () {
    console.log("click en formDARA");
    fetch("/licencias_profesores/")
      .then((response) => response.json())
      .then((licencias) => {
        const divSelection = document.querySelector("#reporte_dara");
        let opcionesLicencias =
          '<option value="">Seleccione una licencia</option>';
        console.log(licencias);

        licencias.forEach((licencia) => {
          opcionesLicencias += `<option value="${licencia.id_licencia}" 
            data-fechaInicio="${licencia.fi}" 
            data-fechaTermino="${licencia.ft}">
            ${licencia.nombre_profesor} con fecha ${licencia.fecha_inicio} hasta ${licencia.fecha_termino}</option>`;
        });
        divSelection.innerHTML = `
          <div class="card mb-3 mx-auto w-50 mt-5">
              <div class="card-body">
                  <h3 class="text-center">Filtro para Informe DARA</h3>
                  <form method="GET" action="{% url 'reportes' %}">
                      <div class="form-group">
                          <div class="mb-3">
                              <label for="licencia">Nombre docente:</label>
                              <select id="licencia" name="licencia" class="form-control" required>
                                  ${opcionesLicencias}
                              </select>
                          </div>
                      </div>
                      <div class="text-center">
                          <button id="btn-filtro-dara" type="button" class="btn btn-success btn-block mt-3" onclick="DARA()">Buscar</button>
                      </div>
                  </form>
              </div>
          </div>
        `;

      })
      .catch((error) => console.error("Error al cargar las licencias:", error));
  });
});

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
      reportSection.innerHTML = "";

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
                              .join(" ")
                      }
                      ${
                        reemplazos.length > 0
                          ? `
                          <tr class="font-weight-bold">
                          </tr>
                          <tr>
                              <td colspan="8" class="font-weight-bold">Horas por Horario:</td>
                              <td>${horas_horarios}</td>
                          </tr>
                          <tr>
                              <td colspan="8" class="font-weight-bold">Horas de Reemplazo:</td>
                              <td>${horas_reemplazo}</td>
                          </tr>
                          <tr>
                              <td colspan="8" class="font-weight-bold">Horas totales:</td>
                              <td>${total_horas}</td>
                          </tr>
                          <tr>
                              <td colspan="8" class="font-weight-bold">Tipo de pago:</td>
                              <td>${tipo_pago}</td>
                          </tr>
                          `
                          : ""
                      }
                  </tbody>
              </table>
          </div>
          <div class="text-center mt-4">
              <button class="btn btn-dark" onclick="emitirInforme()">Emitir Informe</button>
          </div>
      `;

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

async function DARA() {
  const licencia = document.getElementById("licencia");
  const licenciaID = licencia.value;
  const fechaInicio =
    licencia.options[licencia.selectedIndex].getAttribute("data-fechaInicio");
  const fechaTermino =
    licencia.options[licencia.selectedIndex].getAttribute("data-fechaTermino");

  console.log(licenciaID, fechaInicio, "/", fechaTermino);

  if (licenciaID && fechaInicio && fechaTermino) {
    try {
      const response = await fetch(
        `/reporte_dara/?licenciaID=${licenciaID}&fechaInicio=${fechaInicio}&fechaTermino=${fechaTermino}`,
        {
          method: "GET",
          headers: {
            "X-CSRFToken": csrftoken,
          },
        }
      );

      if (!response.ok) {
        throw new Error(`Error al enviar datos: ${response.statusText}`);
      }

      const result = await response.json();
      console.log(result);
    } catch (error) {
      console.error("Error en la solicitud:", error);
    }
  } else {
    console.error("Faltan los parámetros necesarios.");
  }
}
