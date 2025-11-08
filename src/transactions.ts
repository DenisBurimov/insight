document.addEventListener("DOMContentLoaded", function () {
  const clientSelect: HTMLSelectElement = document.querySelector("#client-selected");
  const filtersForm: HTMLFormElement = document.querySelector("#filters-form");
  const ibansInput: HTMLInputElement = document.querySelector("#iban");
  const ibansDiv: HTMLDivElement = document.querySelector("#ibans");
  const accIbans: NodeListOf<HTMLParagraphElement> = document.querySelectorAll(".acc-iban");

  const ownersInput: HTMLInputElement = document.querySelector("#owner");
  const ownersDiv: HTMLDivElement = document.querySelector("#owners");
  const accOwners: NodeListOf<HTMLParagraphElement> = document.querySelectorAll(".acc-owner");


  // On change by clientSelect we submit the filtersForm
  clientSelect.addEventListener("change", function () {
    const edrpouInput: HTMLInputElement  = filtersForm.querySelector('input[name="edrpou"]');
    console.log("edrpouInput", edrpouInput);
    if (edrpouInput) {
        edrpouInput.value = '';
    }
    if (ibansInput) {
        ibansInput.value = '';
    }
    const downloadInput = filtersForm.querySelector('input[name="download"]');
    if (downloadInput) {
        downloadInput.remove();
    }
    filtersForm.submit();
  });

  // On click by ibansInput we toggle the display of ibansDiv
  ibansInput.addEventListener("click", function () {
    ibansDiv.classList.toggle("hidden");
  });

  // On click by each iban we set the value of ibansInput to the clicked iban
  accIbans.forEach((accIban) => {
    accIban.addEventListener("click", function () {
      const iban = accIban.textContent.trim();
      ibansInput.value = iban;
      ibansDiv.classList.add("hidden");
    
      const downloadInput = filtersForm.querySelector('input[name="download"]');
      if (downloadInput) {
          downloadInput.remove();
      }
      filtersForm.submit();
    });
  });

  // ownersInput.addEventListener("click", function () {
  //   ownersDiv.classList.toggle("hidden");
  // });

  // accOwners.forEach((accOwner) => {
  //   accOwner.addEventListener("click", function () {
  //     const owner = accOwner.textContent.trim();
  //     ownersInput.value = owner;
  //     ownersDiv.classList.add("hidden");
  //     filtersForm.submit();
  //   });
  // });
});