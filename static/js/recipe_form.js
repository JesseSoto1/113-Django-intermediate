document.addEventListener('DOMContentLoaded', function() {

    const container = document.getElementById('ingredient-formset-container');
    const addBtn = document.getElementById('add-ingredient-btn');
    const emptyTemplate = document.getElementById('empty-ingredient-form');
    const totalForms = document.querySelector('[name$="-TOTAL_FORMS"]');


    // ADD A NEW INGREDIENT ROW//
    addBtn.addEventListener('click', function () {
        const formIndex = parseInt(totalForms.value);
        const newFormHtml = emptyTemplate.innerHTML.replace(/__prefix__/g, formIndex);
        const wrapper = document.createElement('div');
        wrapper.innerHTML = newFormHtml;
        container.appendChild(wrapper.firstElementChild);
        totalForms.value = formIndex + 1;
    });


    // remove a new (unsaved) row
    // uses event delegation so it works on dynamically added rows too
    container.addEventListener('click', function (e) {
        if (e.target.classList.contains('remove-row-btn')) {
            e.target.closest('.ingredient-row').remove();
            reindexRows();
        }
    });

    // false rows marked for deletion (existing rows)
    container.addEventListener('change', function(e) {
        if (e.target.type === 'checkbox' && e.target.name.includes('DELETE')) {
            const row = e.target.closest('.ingredient-row');
            row.style.capacity = e.target.checked ? '0.4' : '1';

        }
    });


// reindex all rows after a removal
// keep forms indices sequential so Django parse them correctly
    function reindexRows() {
        const rows = container.querySelectorAll('.ingredient-row');

        rows.forEach((row, newIndex) => {
            row.querySelectorAll('input, select').forEach(el => {
                ['name', 'id'].forEach(attr => {
                    const value = el.getAttribute(attr);
                    if (value) {
                        el.setAttribute(attr, value.replace(/-d+-/, `-${newIndex}-`));
                    }
                });
            });
            row.querySelectorAll('label').forEach(Label => {
                const forAttr = Label.getAttribute('for');
                if (forAttr) {
                    label.setAttribute('for', forAttr.replace(/-d+-/, `-${newIndex}-`));
                }
            });
        });

        totalForms.value = rows.length;
    }
})


