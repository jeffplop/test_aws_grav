# ONE PAGE ARCHITECTURE - TIENDA PERRITOS

Todo el proyecto explicado en 1 página.

### [ DESCRIPCIÓN DEL PROYECTO ]
Sistema transaccional de 3 capas contenerizado, orientado a la robustez, orquestado y desplegado de forma 100% remota sobre AWS mediante automatización CI/CD en GitHub Actions.

---

### [ COMPONENTES LÓGICOS ]
1. **Frontend**: Interfaz estática (HTML/JS) servida por Nginx.
2. **Backend**: Lógica de negocios y API REST en Node.js Express.
3. **Persistencia**: Base de datos relacional MySQL 8.0.

---

### [ SEGURIDAD APLICADA ]
*   **Docker Multi-stage**: Separación de las etapas de `builder` vs `production`.
*   **Principio de Menor Privilegio**: Contenedores se ejecutan sin usuario `root`.
*   **Segmentación de Red**: Tráfico encriptado/filtrado por `AWS Security Groups`.

---

### [ DEPLOYMENT PIPELINE ]
`GIT PUSH` -> `GITHUB ACTIONS` -> `DOCKER BUILD` -> `AMAZON ECR` -> `AWS SSM` -> `AMAZON EC2` -> `DOCKER RUN`

---

### [ GESTIÓN DE ESTADO (STATE) ]
Los contenedores son entidades efímeras y *stateless*. Todo el estado real se almacena en Docker *Named Volumes* (`tienda_db_data`), los cuales garantizan su retención fuera del ciclo de vida del contenedor MySQL.
