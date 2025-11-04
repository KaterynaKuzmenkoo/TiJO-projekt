const form = document.getElementById('calc-form');
const statusElement = document.getElementById('status');
const resultBlock = document.getElementById('result-block');
const resultTable = document.getElementById('result-table');
const submitButton = document.getElementById('submit-btn');

const formInputs = {
  gross: document.getElementById('gross'),
  contract: document.getElementById('contract'),
  age: document.getElementById('age'),
  isStudent: document.getElementById('is-student'),
  ulgaMlodzi: document.getElementById('ulga-mlodzi'),
  creative50: document.getElementById('creative-50'),
  kupFixed: document.getElementById('kup-fixed'),
  kupPercent: document.getElementById('kup-percent')
};

function formatMoney(value) {
  const rounded = Math.round((value + 1e-9) * 100) / 100;
  return rounded.toFixed(2).replace('.', ',') + ' PLN';
}

function buildRequestPayload() {
  const payload = {
    gross: Number(formInputs.gross.value),
    contract: formInputs.contract.value,
    age: Number(formInputs.age.value),
    is_student: formInputs.isStudent.checked,
    ulga_mlodzi: formInputs.ulgaMlodzi.checked,
    creative_50: formInputs.creative50.checked
  };

  const kupFixedValue = formInputs.kupFixed.value;
  const kupPercentValue = formInputs.kupPercent.value;

  if (kupFixedValue !== '') {
    payload.kup_fixed = Number(kupFixedValue);
  }

  if (kupPercentValue !== '') {
    payload.kup_percent = Number(kupPercentValue);
  }

  return payload;
}

function createTableRow(label, value) {
  const row = document.createElement('tr');

  const labelCell = document.createElement('td');
  labelCell.textContent = label;

  const valueCell = document.createElement('td');
  valueCell.innerHTML = value;
  valueCell.className = 'right';

  row.appendChild(labelCell);
  row.appendChild(valueCell);

  return row;
}

function displayResults(data) {
  resultTable.innerHTML = '';

  const resultRows = [
    ['Składki społeczne (pracownik)', formatMoney(data.social_total)],
    ['Składka zdrowotna', formatMoney(data.health)],
    ['Koszty uzyskania przychodu (KUP)', formatMoney(data.kup)],
    ['Podstawa PIT', formatMoney(data.pit_base)],
    ['Podatek PIT', formatMoney(data.pit)],
    ['Kwota netto', '<b>' + formatMoney(data.net) + '</b>']
  ];

  resultRows.forEach(([label, value]) => {
    const row = createTableRow(label, value);
    resultTable.appendChild(row);
  });

  resultBlock.classList.remove('hidden');
}

function updateStatus(message) {
  statusElement.textContent = message;
}

function resetUI() {
  submitButton.disabled = true;
  updateStatus('Liczenie…');
  resultBlock.classList.add('hidden');
  resultTable.innerHTML = '';
}

async function handleFormSubmit(event) {
  event.preventDefault();

  resetUI();

  const payload = buildRequestPayload();

  try {
    const response = await fetch('/api/calculate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      throw new Error('Błąd API');
    }

    const data = await response.json();
    displayResults(data);
    updateStatus('Gotowe ✅');
  } catch (error) {
    updateStatus('Wystąpił błąd: ' + error.message);
  } finally {
    submitButton.disabled = false;
  }
}

form.addEventListener('submit', handleFormSubmit);
