$(document).on("click", "#new-ingredient", (e) => {
  e.preventDefault();
  const next = e.currentTarget.dataset.next;
  const ingredientList = document.querySelector("#ingredient-list");
  
  e.currentTarget.remove();

  const newFieldGroup = document.createElement("div");
  newFieldGroup.classList.add("field", "is-grouped");

  const template = `
      <p class="control">
        <input name="ingredient${next}" placeholder="Ingredient Name" class="input" type="text" value="" />
      </p>
      <p class="control">
        <input name="ingredientQuantity${next}" placeholder="Quantity" class="input" type="text" value="" />
      </p>
      <p class="control">
        <input name="ingredientMeasurement${next}" placeholder="Measurement" class="input" type="text" value="" />
      </p>
      <p class="control">
        <button class="input is-primary pl-4 pr-4" id="new-ingredient" data-next="${+next + 1}"><i class="fa fa-plus"></i></button>
      </p>
  `;
  newFieldGroup.innerHTML = template;
  ingredientList.appendChild(newFieldGroup);
});

$(document).on("click", "#new-step", (e) => {
  e.preventDefault();
  const next = e.currentTarget.dataset.next;
  const steps = document.querySelector("#steps");
  
  e.currentTarget.remove();

  const newFieldGroup = document.createElement("div");
  newFieldGroup.classList.add("field", "is-grouped");

  const template = `
      <p class="control is-expanded">
        <input name="step${next}" class="input" type="text" />
      </p>
      <p class="control">
        <button class="input is-primary pl-4 pr-4" id="new-step" data-next="${+next + 1}"><i class="fa fa-plus"></i></button>
      </p>
  `;

  newFieldGroup.innerHTML = template;  
  steps.appendChild(newFieldGroup);
});

