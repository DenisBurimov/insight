/******/ (() => { // webpackBootstrap
/*!*****************************!*\
  !*** ./src/transactions.ts ***!
  \*****************************/
document.addEventListener("DOMContentLoaded", function () {
    var clientSelect = document.querySelector("#client-selected");
    var filtersForm = document.querySelector("#filters-form");
    var ibansInput = document.querySelector("#iban");
    var ibansDiv = document.querySelector("#ibans");
    var accIbans = document.querySelectorAll(".acc-iban");
    var ownersInput = document.querySelector("#owner");
    var ownersDiv = document.querySelector("#owners");
    var accOwners = document.querySelectorAll(".acc-owner");
    // On change by clientSelect we submit the filtersForm
    clientSelect.addEventListener("change", function () {
        var edrpouInput = filtersForm.querySelector('input[name="edrpou"]');
        console.log("edrpouInput", edrpouInput);
        if (edrpouInput) {
            edrpouInput.value = '';
        }
        if (ibansInput) {
            ibansInput.value = '';
        }
        var downloadInput = filtersForm.querySelector('input[name="download"]');
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
    accIbans.forEach(function (accIban) {
        accIban.addEventListener("click", function () {
            var iban = accIban.textContent.trim();
            ibansInput.value = iban;
            ibansDiv.classList.add("hidden");
            var downloadInput = filtersForm.querySelector('input[name="download"]');
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

/******/ })()
;
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoianMvdHJhbnNhY3Rpb25zLmpzIiwibWFwcGluZ3MiOiI7Ozs7QUFBQSxRQUFRLENBQUMsZ0JBQWdCLENBQUMsa0JBQWtCLEVBQUU7SUFDNUMsSUFBTSxZQUFZLEdBQXNCLFFBQVEsQ0FBQyxhQUFhLENBQUMsa0JBQWtCLENBQUMsQ0FBQztJQUNuRixJQUFNLFdBQVcsR0FBb0IsUUFBUSxDQUFDLGFBQWEsQ0FBQyxlQUFlLENBQUMsQ0FBQztJQUM3RSxJQUFNLFVBQVUsR0FBcUIsUUFBUSxDQUFDLGFBQWEsQ0FBQyxPQUFPLENBQUMsQ0FBQztJQUNyRSxJQUFNLFFBQVEsR0FBbUIsUUFBUSxDQUFDLGFBQWEsQ0FBQyxRQUFRLENBQUMsQ0FBQztJQUNsRSxJQUFNLFFBQVEsR0FBcUMsUUFBUSxDQUFDLGdCQUFnQixDQUFDLFdBQVcsQ0FBQyxDQUFDO0lBRTFGLElBQU0sV0FBVyxHQUFxQixRQUFRLENBQUMsYUFBYSxDQUFDLFFBQVEsQ0FBQyxDQUFDO0lBQ3ZFLElBQU0sU0FBUyxHQUFtQixRQUFRLENBQUMsYUFBYSxDQUFDLFNBQVMsQ0FBQyxDQUFDO0lBQ3BFLElBQU0sU0FBUyxHQUFxQyxRQUFRLENBQUMsZ0JBQWdCLENBQUMsWUFBWSxDQUFDLENBQUM7SUFHNUYsc0RBQXNEO0lBQ3RELFlBQVksQ0FBQyxnQkFBZ0IsQ0FBQyxRQUFRLEVBQUU7UUFDdEMsSUFBTSxXQUFXLEdBQXNCLFdBQVcsQ0FBQyxhQUFhLENBQUMsc0JBQXNCLENBQUMsQ0FBQztRQUN6RixPQUFPLENBQUMsR0FBRyxDQUFDLGFBQWEsRUFBRSxXQUFXLENBQUMsQ0FBQztRQUN4QyxJQUFJLFdBQVcsRUFBRTtZQUNiLFdBQVcsQ0FBQyxLQUFLLEdBQUcsRUFBRSxDQUFDO1NBQzFCO1FBQ0QsSUFBSSxVQUFVLEVBQUU7WUFDWixVQUFVLENBQUMsS0FBSyxHQUFHLEVBQUUsQ0FBQztTQUN6QjtRQUNELElBQU0sYUFBYSxHQUFHLFdBQVcsQ0FBQyxhQUFhLENBQUMsd0JBQXdCLENBQUMsQ0FBQztRQUMxRSxJQUFJLGFBQWEsRUFBRTtZQUNmLGFBQWEsQ0FBQyxNQUFNLEVBQUUsQ0FBQztTQUMxQjtRQUNELFdBQVcsQ0FBQyxNQUFNLEVBQUUsQ0FBQztJQUN2QixDQUFDLENBQUMsQ0FBQztJQUVILDJEQUEyRDtJQUMzRCxVQUFVLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFO1FBQ25DLFFBQVEsQ0FBQyxTQUFTLENBQUMsTUFBTSxDQUFDLFFBQVEsQ0FBQyxDQUFDO0lBQ3RDLENBQUMsQ0FBQyxDQUFDO0lBRUgsMkVBQTJFO0lBQzNFLFFBQVEsQ0FBQyxPQUFPLENBQUMsVUFBQyxPQUFPO1FBQ3ZCLE9BQU8sQ0FBQyxnQkFBZ0IsQ0FBQyxPQUFPLEVBQUU7WUFDaEMsSUFBTSxJQUFJLEdBQUcsT0FBTyxDQUFDLFdBQVcsQ0FBQyxJQUFJLEVBQUUsQ0FBQztZQUN4QyxVQUFVLENBQUMsS0FBSyxHQUFHLElBQUksQ0FBQztZQUN4QixRQUFRLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLENBQUMsQ0FBQztZQUVqQyxJQUFNLGFBQWEsR0FBRyxXQUFXLENBQUMsYUFBYSxDQUFDLHdCQUF3QixDQUFDLENBQUM7WUFDMUUsSUFBSSxhQUFhLEVBQUU7Z0JBQ2YsYUFBYSxDQUFDLE1BQU0sRUFBRSxDQUFDO2FBQzFCO1lBQ0QsV0FBVyxDQUFDLE1BQU0sRUFBRSxDQUFDO1FBQ3ZCLENBQUMsQ0FBQyxDQUFDO0lBQ0wsQ0FBQyxDQUFDLENBQUM7SUFFSCxzREFBc0Q7SUFDdEQsMENBQTBDO0lBQzFDLE1BQU07SUFFTixvQ0FBb0M7SUFDcEMscURBQXFEO0lBQ3JELGlEQUFpRDtJQUNqRCxpQ0FBaUM7SUFDakMseUNBQXlDO0lBQ3pDLDRCQUE0QjtJQUM1QixRQUFRO0lBQ1IsTUFBTTtBQUNSLENBQUMsQ0FBQyxDQUFDIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vc3RhdGljLy4vc3JjL3RyYW5zYWN0aW9ucy50cyJdLCJzb3VyY2VzQ29udGVudCI6WyJkb2N1bWVudC5hZGRFdmVudExpc3RlbmVyKFwiRE9NQ29udGVudExvYWRlZFwiLCBmdW5jdGlvbiAoKSB7XG4gIGNvbnN0IGNsaWVudFNlbGVjdDogSFRNTFNlbGVjdEVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2NsaWVudC1zZWxlY3RlZFwiKTtcbiAgY29uc3QgZmlsdGVyc0Zvcm06IEhUTUxGb3JtRWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjZmlsdGVycy1mb3JtXCIpO1xuICBjb25zdCBpYmFuc0lucHV0OiBIVE1MSW5wdXRFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNpYmFuXCIpO1xuICBjb25zdCBpYmFuc0RpdjogSFRNTERpdkVsZW1lbnQgPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yKFwiI2liYW5zXCIpO1xuICBjb25zdCBhY2NJYmFuczogTm9kZUxpc3RPZjxIVE1MUGFyYWdyYXBoRWxlbWVudD4gPSBkb2N1bWVudC5xdWVyeVNlbGVjdG9yQWxsKFwiLmFjYy1pYmFuXCIpO1xuXG4gIGNvbnN0IG93bmVyc0lucHV0OiBIVE1MSW5wdXRFbGVtZW50ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvcihcIiNvd25lclwiKTtcbiAgY29uc3Qgb3duZXJzRGl2OiBIVE1MRGl2RWxlbWVudCA9IGRvY3VtZW50LnF1ZXJ5U2VsZWN0b3IoXCIjb3duZXJzXCIpO1xuICBjb25zdCBhY2NPd25lcnM6IE5vZGVMaXN0T2Y8SFRNTFBhcmFncmFwaEVsZW1lbnQ+ID0gZG9jdW1lbnQucXVlcnlTZWxlY3RvckFsbChcIi5hY2Mtb3duZXJcIik7XG5cblxuICAvLyBPbiBjaGFuZ2UgYnkgY2xpZW50U2VsZWN0IHdlIHN1Ym1pdCB0aGUgZmlsdGVyc0Zvcm1cbiAgY2xpZW50U2VsZWN0LmFkZEV2ZW50TGlzdGVuZXIoXCJjaGFuZ2VcIiwgZnVuY3Rpb24gKCkge1xuICAgIGNvbnN0IGVkcnBvdUlucHV0OiBIVE1MSW5wdXRFbGVtZW50ICA9IGZpbHRlcnNGb3JtLnF1ZXJ5U2VsZWN0b3IoJ2lucHV0W25hbWU9XCJlZHJwb3VcIl0nKTtcbiAgICBjb25zb2xlLmxvZyhcImVkcnBvdUlucHV0XCIsIGVkcnBvdUlucHV0KTtcbiAgICBpZiAoZWRycG91SW5wdXQpIHtcbiAgICAgICAgZWRycG91SW5wdXQudmFsdWUgPSAnJztcbiAgICB9XG4gICAgaWYgKGliYW5zSW5wdXQpIHtcbiAgICAgICAgaWJhbnNJbnB1dC52YWx1ZSA9ICcnO1xuICAgIH1cbiAgICBjb25zdCBkb3dubG9hZElucHV0ID0gZmlsdGVyc0Zvcm0ucXVlcnlTZWxlY3RvcignaW5wdXRbbmFtZT1cImRvd25sb2FkXCJdJyk7XG4gICAgaWYgKGRvd25sb2FkSW5wdXQpIHtcbiAgICAgICAgZG93bmxvYWRJbnB1dC5yZW1vdmUoKTtcbiAgICB9XG4gICAgZmlsdGVyc0Zvcm0uc3VibWl0KCk7XG4gIH0pO1xuXG4gIC8vIE9uIGNsaWNrIGJ5IGliYW5zSW5wdXQgd2UgdG9nZ2xlIHRoZSBkaXNwbGF5IG9mIGliYW5zRGl2XG4gIGliYW5zSW5wdXQuYWRkRXZlbnRMaXN0ZW5lcihcImNsaWNrXCIsIGZ1bmN0aW9uICgpIHtcbiAgICBpYmFuc0Rpdi5jbGFzc0xpc3QudG9nZ2xlKFwiaGlkZGVuXCIpO1xuICB9KTtcblxuICAvLyBPbiBjbGljayBieSBlYWNoIGliYW4gd2Ugc2V0IHRoZSB2YWx1ZSBvZiBpYmFuc0lucHV0IHRvIHRoZSBjbGlja2VkIGliYW5cbiAgYWNjSWJhbnMuZm9yRWFjaCgoYWNjSWJhbikgPT4ge1xuICAgIGFjY0liYW4uYWRkRXZlbnRMaXN0ZW5lcihcImNsaWNrXCIsIGZ1bmN0aW9uICgpIHtcbiAgICAgIGNvbnN0IGliYW4gPSBhY2NJYmFuLnRleHRDb250ZW50LnRyaW0oKTtcbiAgICAgIGliYW5zSW5wdXQudmFsdWUgPSBpYmFuO1xuICAgICAgaWJhbnNEaXYuY2xhc3NMaXN0LmFkZChcImhpZGRlblwiKTtcbiAgICBcbiAgICAgIGNvbnN0IGRvd25sb2FkSW5wdXQgPSBmaWx0ZXJzRm9ybS5xdWVyeVNlbGVjdG9yKCdpbnB1dFtuYW1lPVwiZG93bmxvYWRcIl0nKTtcbiAgICAgIGlmIChkb3dubG9hZElucHV0KSB7XG4gICAgICAgICAgZG93bmxvYWRJbnB1dC5yZW1vdmUoKTtcbiAgICAgIH1cbiAgICAgIGZpbHRlcnNGb3JtLnN1Ym1pdCgpO1xuICAgIH0pO1xuICB9KTtcblxuICAvLyBvd25lcnNJbnB1dC5hZGRFdmVudExpc3RlbmVyKFwiY2xpY2tcIiwgZnVuY3Rpb24gKCkge1xuICAvLyAgIG93bmVyc0Rpdi5jbGFzc0xpc3QudG9nZ2xlKFwiaGlkZGVuXCIpO1xuICAvLyB9KTtcblxuICAvLyBhY2NPd25lcnMuZm9yRWFjaCgoYWNjT3duZXIpID0+IHtcbiAgLy8gICBhY2NPd25lci5hZGRFdmVudExpc3RlbmVyKFwiY2xpY2tcIiwgZnVuY3Rpb24gKCkge1xuICAvLyAgICAgY29uc3Qgb3duZXIgPSBhY2NPd25lci50ZXh0Q29udGVudC50cmltKCk7XG4gIC8vICAgICBvd25lcnNJbnB1dC52YWx1ZSA9IG93bmVyO1xuICAvLyAgICAgb3duZXJzRGl2LmNsYXNzTGlzdC5hZGQoXCJoaWRkZW5cIik7XG4gIC8vICAgICBmaWx0ZXJzRm9ybS5zdWJtaXQoKTtcbiAgLy8gICB9KTtcbiAgLy8gfSk7XG59KTsiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=