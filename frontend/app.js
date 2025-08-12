const apiBase = "http://localhost:5000/api";

let pacientes = [];
let medicos = [];
let citas = [];
let paginaActual = 1;
const citasPorPagina = 10;
let totalPaginas = 1;

// --------------- PACIENTES ----------------
async function fetchPacientes() {
  const res = await fetch(`${apiBase}/pacientes`);
  pacientes = await res.json();
  renderPacientes();
  renderPacienteOptions();
}

function renderPacientes() {
  const ul = document.getElementById("lista-pacientes");
  ul.innerHTML = "";
  pacientes.forEach(p => {
    const li = document.createElement("li");
    li.innerHTML = `
      ${p.nombre} ${p.apellido} - Nac: ${p.fecha_nacimiento} - Email: ${p.email}
      <button class="btn-edit" data-id="${p.id}">Editar</button>
      <button class="btn-delete" data-id="${p.id}">Eliminar</button>
      <div class="edit-form" id="edit-form-paciente-${p.id}" style="display:none; margin-top:8px;">
        <input type="text" id="edit-nombre-${p.id}" value="${p.nombre}" />
        <input type="text" id="edit-apellido-${p.id}" value="${p.apellido}" />
        <input type="date" id="edit-fecha-${p.id}" value="${p.fecha_nacimiento}" />
        <input type="email" id="edit-email-${p.id}" value="${p.email}" />
        <button class="btn-save" data-id="${p.id}" data-type="paciente">Guardar</button>
        <button class="btn-cancel" data-id="${p.id}" data-type="paciente">Cancelar</button>
      </div>
    `;
    ul.appendChild(li);
  });
}

function renderPacienteOptions() {
  const select = document.getElementById("cita-paciente");
  select.innerHTML = "";
  pacientes.forEach(p => {
    const opt = document.createElement("option");
    opt.value = p.id;
    opt.textContent = `${p.nombre} ${p.apellido}`;
    select.appendChild(opt);
  });
}

document.getElementById("form-paciente").addEventListener("submit", async e => {
  e.preventDefault();
  const nombre = document.getElementById("paciente-nombre").value.trim();
  const apellido = document.getElementById("paciente-apellido").value.trim();
  const fecha_nacimiento = document.getElementById("paciente-fecha").value;
  const email = document.getElementById("paciente-email").value.trim();

  const res = await fetch(`${apiBase}/pacientes`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ nombre, apellido, fecha_nacimiento, email })
  });

  if(res.ok){
    const nuevo = await res.json();
    pacientes.push(nuevo);
    renderPacientes();
    renderPacienteOptions();
    e.target.reset();
  } else {
    alert("Error agregando paciente");
  }
});

document.getElementById("lista-pacientes").addEventListener("click", async e => {
  const id = e.target.dataset.id;
  if(!id) return;

  if(e.target.classList.contains("btn-edit")){
    document.getElementById(`edit-form-paciente-${id}`).style.display = "block";
  }
  else if(e.target.classList.contains("btn-cancel")){
    document.getElementById(`edit-form-paciente-${id}`).style.display = "none";
  }
  else if(e.target.classList.contains("btn-save")){
    const nombre = document.getElementById(`edit-nombre-${id}`).value.trim();
    const apellido = document.getElementById(`edit-apellido-${id}`).value.trim();
    const fecha_nacimiento = document.getElementById(`edit-fecha-${id}`).value;
    const email = document.getElementById(`edit-email-${id}`).value.trim();

    const res = await fetch(`${apiBase}/pacientes/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ nombre, apellido, fecha_nacimiento, email })
    });

    if(res.ok){
      await fetchPacientes();
    } else {
      alert("Error actualizando paciente");
    }
  }
  else if(e.target.classList.contains("btn-delete")){
    if(confirm("¿Seguro que quieres eliminar este paciente?")){
      const res = await fetch(`${apiBase}/pacientes/${id}`, { method: "DELETE" });
      if(res.ok){
        await fetchPacientes();
      } else {
        alert("Error eliminando paciente");
      }
    }
  }
});

// --------------- MÉDICOS ----------------
async function fetchMedicos() {
  const res = await fetch(`${apiBase}/medicos`);
  medicos = await res.json();
  renderMedicos();
  renderMedicoOptions();
}

function renderMedicos() {
  const ul = document.getElementById("lista-medicos");
  ul.innerHTML = "";
  medicos.forEach(m => {
    const li = document.createElement("li");
    li.innerHTML = `
      ${m.nombre} ${m.apellido} - ${m.especialidad}
      <button class="btn-edit" data-id="${m.id}">Editar</button>
      <button class="btn-delete" data-id="${m.id}">Eliminar</button>
      <div class="edit-form" id="edit-form-medico-${m.id}" style="display:none; margin-top:8px;">
        <input type="text" id="edit-nombre-m-${m.id}" value="${m.nombre}" />
        <input type="text" id="edit-apellido-m-${m.id}" value="${m.apellido}" />
        <input type="text" id="edit-especialidad-m-${m.id}" value="${m.especialidad}" />
        <button class="btn-save" data-id="${m.id}" data-type="medico">Guardar</button>
        <button class="btn-cancel" data-id="${m.id}" data-type="medico">Cancelar</button>
      </div>
    `;
    ul.appendChild(li);
  });
}

function renderMedicoOptions() {
  const select = document.getElementById("cita-medico");
  select.innerHTML = "";
  medicos.forEach(m => {
    const opt = document.createElement("option");
    opt.value = m.id;
    opt.textContent = `${m.nombre} - ${m.especialidad}`;
    select.appendChild(opt);
  });
}

document.getElementById("form-medico").addEventListener("submit", async e => {
  e.preventDefault();
  const nombre = document.getElementById("medico-nombre").value.trim();
  const apellido = "";  // No tienes input apellido en el formulario para agregar, pero backend lo pide
  const especialidad = document.getElementById("medico-especialidad").value.trim();

  // Si necesitas apellido, agrega un campo en el formulario
  // Aquí voy a agregar apellido vacío para que no falle
  const res = await fetch(`${apiBase}/medicos`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ nombre, apellido, especialidad })
  });

  if(res.ok){
    const nuevo = await res.json();
    medicos.push(nuevo);
    renderMedicos();
    renderMedicoOptions();
    e.target.reset();
  } else {
    alert("Error agregando médico");
  }
});

document.getElementById("lista-medicos").addEventListener("click", async e => {
  const id = e.target.dataset.id;
  if(!id) return;

  if(e.target.classList.contains("btn-edit")){
    document.getElementById(`edit-form-medico-${id}`).style.display = "block";
  }
  else if(e.target.classList.contains("btn-cancel")){
    document.getElementById(`edit-form-medico-${id}`).style.display = "none";
  }
  else if(e.target.classList.contains("btn-save")){
    const nombre = document.getElementById(`edit-nombre-m-${id}`).value.trim();
    const apellido = document.getElementById(`edit-apellido-m-${id}`)?.value.trim() || "";
    const especialidad = document.getElementById(`edit-especialidad-m-${id}`).value.trim();

    const res = await fetch(`${apiBase}/medicos/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ nombre, apellido, especialidad })
    });

    if(res.ok){
      await fetchMedicos();
    } else {
      alert("Error actualizando médico");
    }
  }
  else if(e.target.classList.contains("btn-delete")){
    if(confirm("¿Seguro que quieres eliminar este médico?")){
      const res = await fetch(`${apiBase}/medicos/${id}`, { method: "DELETE" });
      if(res.ok){
        await fetchMedicos();
      } else {
        alert("Error eliminando médico");
      }
    }
  }
});

// --------------- CITAS ----------------
async function fetchCitas(page = 1) {
  const res = await fetch(`${apiBase}/citas?page=${page}`);
  if(!res.ok){
    alert("Error obteniendo citas");
    return;
  }
  const data = await res.json();
  citas = data.citas;
  paginaActual = data.current_page;
  totalPaginas = data.pages;
  renderCitas();
  document.getElementById("pagina-info").textContent = `Página ${paginaActual} de ${totalPaginas}`;
}

function renderCitas() {
  const ul = document.getElementById("lista-citas");
  ul.innerHTML = "";
  citas.forEach(c => {
    const paciente = pacientes.find(p => p.id === c.paciente_id);
    const medico = medicos.find(m => m.id === c.medico_id);
    const pacienteNombre = paciente ? `${paciente.nombre} ${paciente.apellido}` : "Paciente no encontrado";
    const medicoNombre = medico ? `${medico.nombre} ${medico.apellido} (${medico.especialidad})` : "Médico no encontrado";

    const li = document.createElement("li");
    li.innerHTML = `
      ${pacienteNombre} con ${medicoNombre} - ${c.fecha} ${c.hora} - Consultorio: ${c.consultorio || ""}
      <button class="btn-edit" data-id="${c.id}">Editar</button>
      <button class="btn-delete" data-id="${c.id}">Eliminar</button>
      <div class="edit-form" id="edit-form-cita-${c.id}" style="display:none; margin-top:8px;">
        <select id="edit-paciente-cita-${c.id}"></select>
        <select id="edit-medico-cita-${c.id}"></select>
        <input type="date" id="edit-fecha-cita-${c.id}" value="${c.fecha}" />
        <input type="time" id="edit-hora-cita-${c.id}" value="${c.hora.substring(0,5)}" />
        <input type="text" id="edit-consultorio-cita-${c.id}" value="${c.consultorio || ""}" placeholder="Consultorio"/>
        <button class="btn-save" data-id="${c.id}" data-type="cita">Guardar</button>
        <button class="btn-cancel" data-id="${c.id}" data-type="cita">Cancelar</button>
      </div>
    `;
    ul.appendChild(li);

    // Render opciones de paciente y medico dentro del edit-form select
    const pacienteSelect = document.getElementById(`edit-paciente-cita-${c.id}`);
    pacientes.forEach(p => {
      const opt = document.createElement("option");
      opt.value = p.id;
      opt.textContent = `${p.nombre} ${p.apellido}`;
      if(p.id === c.paciente_id) opt.selected = true;
      pacienteSelect.appendChild(opt);
    });

    const medicoSelect = document.getElementById(`edit-medico-cita-${c.id}`);
    medicos.forEach(m => {
      const opt = document.createElement("option");
      opt.value = m.id;
      opt.textContent = `${m.nombre} - ${m.especialidad}`;
      if(m.id === c.medico_id) opt.selected = true;
      medicoSelect.appendChild(opt);
    });
  });
}

document.getElementById("form-cita").addEventListener("submit", async e => {
  e.preventDefault();
  const paciente_id = parseInt(document.getElementById("cita-paciente").value);
  const medico_id = parseInt(document.getElementById("cita-medico").value);
  const fechaHora = document.getElementById("cita-fecha").value;
  if (!fechaHora) {
    alert("Seleccione fecha y hora");
    return;
  }
  const fecha = fechaHora.split("T")[0];
  const hora = fechaHora.split("T")[1] + ":00";

  const res = await fetch(`${apiBase}/citas`, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ paciente_id, medico_id, fecha, hora })
  });

  if(res.ok){
    const nueva = await res.json();
    citas.push(nueva);
    await fetchCitas(paginaActual); // refresca la pagina actual
    e.target.reset();
  } else {
    alert("Error agregando cita");
  }
});

document.getElementById("lista-citas").addEventListener("click", async e => {
  const id = e.target.dataset.id;
  if(!id) return;

  if(e.target.classList.contains("btn-edit")){
    document.getElementById(`edit-form-cita-${id}`).style.display = "block";
  }
  else if(e.target.classList.contains("btn-cancel")){
    document.getElementById(`edit-form-cita-${id}`).style.display = "none";
  }
  else if(e.target.classList.contains("btn-save")){
    const paciente_id = parseInt(document.getElementById(`edit-paciente-cita-${id}`).value);
    const medico_id = parseInt(document.getElementById(`edit-medico-cita-${id}`).value);
    const fecha = document.getElementById(`edit-fecha-cita-${id}`).value;
    const hora = document.getElementById(`edit-hora-cita-${id}`).value + ":00";
    const consultorio = document.getElementById(`edit-consultorio-cita-${id}`).value.trim();

    const res = await fetch(`${apiBase}/citas/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({ paciente_id, medico_id, fecha, hora, consultorio })
    });

    if(res.ok){
      await fetchCitas(paginaActual);
    } else {
      alert("Error actualizando cita");
    }
  }
  else if(e.target.classList.contains("btn-delete")){
    if(confirm("¿Seguro que quieres eliminar esta cita?")){
      const res = await fetch(`${apiBase}/citas/${id}`, { method: "DELETE" });
      if(res.ok){
        await fetchCitas(paginaActual);
      } else {
        alert("Error eliminando cita");
      }
    }
  }
});

// --------------- PAGINACIÓN CITAS ---------------
document.getElementById("prev-page").addEventListener("click", () => {
  if (paginaActual > 1) fetchCitas(paginaActual - 1);
});
document.getElementById("next-page").addEventListener("click", () => {
  if (paginaActual < totalPaginas) fetchCitas(paginaActual + 1);
});

// --------------- INICIALIZAR ---------------
async function init() {
  await fetchPacientes();
  await fetchMedicos();
  await fetchCitas();
}
init();
