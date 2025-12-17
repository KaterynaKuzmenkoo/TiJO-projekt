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
  youthTaxRelief: document.getElementById('ulga-mlodzi'),
  creative50: document.getElementById('creative-50'),
  taxDeductibleFixed: document.getElementById('kup-fixed'),
  taxDeductiblePercent: document.getElementById('kup-percent')
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
    youth_tax_relief: formInputs.youthTaxRelief.checked,
    creative_50: formInputs.creative50.checked
  };

  const taxDeductibleFixedValue = formInputs.taxDeductibleFixed.value;
  const taxDeductiblePercentValue = formInputs.taxDeductiblePercent.value;

  if (taxDeductibleFixedValue !== '') {
    payload.tax_deductible_fixed = Number(taxDeductibleFixedValue);
  }

  if (taxDeductiblePercentValue !== '') {
    payload.tax_deductible_percent = Number(taxDeductiblePercentValue);
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
    ['Koszty uzyskania przychodu (KUP)', formatMoney(data.tax_deductible_costs)],
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
