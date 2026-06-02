document.addEventListener("DOMContentLoaded", () => {
    const toggleButtons = document.querySelectorAll("[data-table-toggle]");
    const activeTable = document.getElementById("tabela-ativos");
    const inactiveTable = document.getElementById("tabela-inativos");

    if (toggleButtons.length && activeTable && inactiveTable) {
        toggleButtons.forEach((button) => {
            button.addEventListener("click", () => {
                const tableType = button.dataset.tableToggle;
                const showActive = tableType === "ativos";

                activeTable.classList.toggle("hidden", !showActive);
                inactiveTable.classList.toggle("hidden", showActive);

                toggleButtons.forEach((item) => item.classList.remove("active"));
                button.classList.add("active");
            });
        });
    }

    const openPanel = (panelId) => {
        const panel = document.getElementById(panelId);

        if (!panel) {
            return;
        }

        document.querySelectorAll(".action-panel").forEach((item) => {
            item.classList.toggle("is-open", item === panel);
        });

        document.querySelectorAll("[data-panel-target]").forEach((button) => {
            button.classList.toggle("active", button.dataset.panelTarget === panelId);
        });

        panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
    };

    document.querySelectorAll("[data-panel-target]").forEach((button) => {
        button.addEventListener("click", () => openPanel(button.dataset.panelTarget));
    });

    document.querySelectorAll("[data-panel-close]").forEach((button) => {
        button.addEventListener("click", () => {
            const panel = button.closest(".action-panel");

            if (panel) {
                panel.classList.remove("is-open");
            }

            document.querySelectorAll("[data-panel-target]").forEach((item) => {
                if (panel && item.dataset.panelTarget === panel.id) {
                    item.classList.remove("active");
                }
            });
        });
    });

    document.querySelectorAll("[data-fill-material-edit]").forEach((button) => {
        button.addEventListener("click", () => {
            const idField = document.getElementById("id_material_edicao");
            const nameField = document.getElementById("nome_edicao");
            const minimumField = document.getElementById("quantidade_minima_edicao");

            if (idField) {
                idField.value = button.dataset.id;
            }

            if (nameField) {
                nameField.value = button.dataset.nome;
            }

            if (minimumField) {
                minimumField.value = button.dataset.minima;
            }
        });
    });

    document.querySelectorAll("[data-fill-user-edit]").forEach((button) => {
        button.addEventListener("click", () => {
            const idField = document.getElementById("id_usuario_edicao");
            const nameField = document.getElementById("nome_edicao");
            const emailField = document.getElementById("email_edicao");
            const profileField = document.getElementById("perfil_edicao");

            if (idField) {
                idField.value = button.dataset.id;
            }

            if (nameField) {
                nameField.value = button.dataset.nome;
            }

            if (emailField) {
                emailField.value = button.dataset.email;
            }

            if (profileField) {
                profileField.value = button.dataset.perfil;
            }
        });
    });

    document.querySelectorAll("[data-table-search]").forEach((input) => {
        const targets = input.dataset.searchTarget
            .split(",")
            .map((selector) => selector.trim())
            .filter(Boolean);
        const tools = document.createElement("div");
        const counter = document.createElement("span");
        const clearButton = document.createElement("button");

        tools.className = "search-tools";
        counter.className = "search-counter";
        clearButton.className = "search-clear";
        clearButton.type = "button";
        clearButton.textContent = "Limpar pesquisa";
        tools.append(counter, clearButton);
        input.closest(".search-bar").appendChild(tools);

        const updateSearch = () => {
            const searchTerm = input.value.trim().toLowerCase();
            let visibleRows = 0;
            let totalRows = 0;

            targets.forEach((selector) => {
                const tableArea = document.querySelector(selector);

                if (!tableArea) {
                    return;
                }

                const rows = tableArea.querySelectorAll("tbody tr");

                rows.forEach((row) => {
                    if (row.querySelector(".empty-state")) {
                        return;
                    }

                    const rowText = row.textContent.toLowerCase();
                    const shouldHide = Boolean(searchTerm && !rowText.includes(searchTerm));
                    row.classList.toggle("hidden-row", shouldHide);
                    totalRows += 1;

                    if (!shouldHide) {
                        visibleRows += 1;
                    }
                });
            });

            counter.textContent = searchTerm
                ? `${visibleRows} de ${totalRows} resultado(s)`
                : `${totalRows} item(ns) na lista`;

            input.closest(".search-bar").classList.toggle("no-results", Boolean(searchTerm && visibleRows === 0));
        };

        input.addEventListener("input", updateSearch);
        clearButton.addEventListener("click", () => {
            input.value = "";
            updateSearch();
            input.focus();
        });

        updateSearch();
    });

    document.querySelectorAll("[data-modal-target]").forEach((button) => {
        button.addEventListener("click", () => {
            const modal = document.getElementById(button.dataset.modalTarget);

            if (modal) {
                modal.classList.add("is-open");
                modal.setAttribute("aria-hidden", "false");
            }
        });
    });

    document.querySelectorAll("[data-modal-close]").forEach((button) => {
        button.addEventListener("click", () => {
            const modal = button.closest(".modal-overlay");

            if (modal) {
                modal.classList.remove("is-open");
                modal.setAttribute("aria-hidden", "true");
            }
        });
    });

    document.querySelectorAll(".modal-overlay").forEach((modal) => {
        modal.addEventListener("click", (event) => {
            if (event.target === modal) {
                modal.classList.remove("is-open");
                modal.setAttribute("aria-hidden", "true");
            }
        });
    });

    let pendingForm = null;
    const confirmModal = document.getElementById("confirm-modal");
    const confirmMessage = document.getElementById("confirm-message");
    const confirmSubmit = document.querySelector("[data-confirm-submit]");
    const confirmCancelButtons = document.querySelectorAll("[data-confirm-cancel]");

    document.querySelectorAll("form[data-confirm]").forEach((form) => {
        form.addEventListener("submit", (event) => {
            event.preventDefault();
            pendingForm = form;

            if (confirmMessage) {
                confirmMessage.textContent = form.dataset.confirm;
            }

            if (confirmModal) {
                confirmModal.classList.add("is-open");
                confirmModal.setAttribute("aria-hidden", "false");
            }
        });
    });

    confirmCancelButtons.forEach((button) => {
        button.addEventListener("click", () => {
            pendingForm = null;

            if (confirmModal) {
                confirmModal.classList.remove("is-open");
                confirmModal.setAttribute("aria-hidden", "true");
            }
        });
    });

    if (confirmSubmit) {
        confirmSubmit.addEventListener("click", () => {
            if (!pendingForm) {
                return;
            }

            pendingForm.removeAttribute("data-confirm");
            pendingForm.submit();
        });
    }

    document.querySelectorAll("form").forEach((form) => {
        form.addEventListener("submit", () => {
            const button = form.querySelector("button[type='submit']");

            if (!button || form.dataset.confirm) {
                return;
            }

            button.dataset.originalText = button.textContent;
            button.textContent = "Salvando...";
            button.disabled = true;
            form.classList.add("is-submitting");
        });
    });
});
