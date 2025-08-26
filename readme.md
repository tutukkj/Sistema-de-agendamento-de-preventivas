![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Selenium](https://img.shields.io/badge/Selenium-Automation-43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-11557C?style=for-the-badge&logo=plotly&logoColor=white)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI%20Toolkit-FF6F00?style=for-the-badge)
![WhatsApp](https://img.shields.io/badge/WhatsApp%20Automation-25D366?style=for-the-badge&logo=whatsapp&logoColor=white)
![Planilhas Excel](https://img.shields.io/badge/Excel%20Automation-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Produção-brightgreen?style=for-the-badge)

# 📡 Sistema de Envio e Monitoramento de Mensagens no WhatsApp

Uma solução automatizada desenvolvida em **Python** para **envio em
massa de mensagens via WhatsApp Web**, **monitoramento de respostas** e
**agendamento automático de manutenções preventivas** no sistema
Segware.\
O sistema foi projetado para otimizar processos internos e garantir a
rastreabilidade completa de interações com clientes.

------------------------------------------------------------------------

## 🧠 Tecnologias e Bibliotecas

-   **Selenium**: Automação do WhatsApp Web e do sistema Segware.\
-   **Pandas**: Manipulação de dados da planilha Excel.\
-   **Matplotlib**: Visualização em tempo real do progresso de envio.\
-   **Tkinter**: Interface gráfica amigável.\
-   **gspread**: Integração com planilhas do Google.\
-   **webdriver_manager**: Gerenciamento automático do ChromeDriver.\
-   **PyAutoGUI** *(versão anterior)*: Automação de processos manuais.

------------------------------------------------------------------------

## 📸 Demonstração / Prints

```{=html}
<!-- Adicione aqui os prints da interface gráfica e do WhatsApp Web automatizado -->
```
![Interface Principal](link-para-screenshot1.png)
![Monitoramento](link-para-screenshot2.png) ![Progresso do
Envio](link-para-screenshot3.png)

------------------------------------------------------------------------

## 🚀 Funcionalidades

1.  **Envio Automático de Mensagens**
    -   Lê os dados de clientes a partir de uma planilha Excel.\
    -   Envia mensagens personalizadas com base no tipo de manutenção
        (Portão ou Sistema).\
    -   Apresenta barra de progresso em tempo real.
2.  **Monitoramento de Conversas**
    -   Identifica respostas automáticas (SIM/NÃO).\
    -   Atualiza a planilha com o status detalhado da mensagem (Enviado,
        Entregue, Lido).\
    -   Registra todas as interações em um log.
3.  **Agendamento Automático no Segware**
    -   Lê a planilha atualizada com as respostas.\
    -   Preenche automaticamente os campos no sistema Segware para
        agendar manutenções.
4.  **Interface Simples**
    -   Interface gráfica com botões intuitivos para seleção da planilha
        e controle do monitoramento.

------------------------------------------------------------------------

## 📂 Estrutura do Projeto

    .
    ├── sendwhats.py           # Sistema de envio e monitoramento via WhatsApp
    ├── os.py                  # Automação do agendamento no Segware
    ├── Manuntenção-Preventiva.xlsx  # Planilha de exemplo (não incluída)
    └── README.md              # Este arquivo

------------------------------------------------------------------------

## ⚙️ Como Rodar a Aplicação

### 1 Clone o repositório

``` bash
git clone <url-do-repositorio>
cd <pasta-do-projeto>
```


### 2 Instale as dependências

``` bash
pip install -r requirements.txt
```

### 3 Execute a interface de envio

``` bash
python sendwhats.py
```

### 5 Execute o agendamento no Segware

``` bash
python os.py
```

------------------------------------------------------------------------

## 📊 Fluxo de Funcionamento

1.  Selecione a planilha de clientes na interface gráfica.\
2.  Escaneie o QR Code do WhatsApp Web.\
3.  O sistema envia as mensagens e monitora as respostas.\
4.  Após finalização, atualize os dados da planilha.\
5.  Execute o script `os.py` para que os agendamentos sejam realizados
    automaticamente.

------------------------------------------------------------------------

## 📝 Exemplo de Planilha

  -------------------------------------------------------------------------------------------------------------------
  Cliente   Conta   Data         Numero          Tipo         Resposta     Status      URL                  Técnico
                                                 Manutenção   Monitorada   Detalhado                        
  --------- ------- ------------ --------------- ------------ ------------ ----------- -------------------- ---------
  ACME      12345   01/09/2025   +551199999999   Portão       SIM          Lido        https://segware...   ROGER

  XPTO      54321   02/09/2025   +551198888888   Sistema      NÃO          Entregue    https://segware...   IGOR
  -------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

## 📜 Licença

Este projeto é **interno e confidencial**, não possuindo licença
pública.

------------------------------------------------------------------------

## ✨ Autor

Desenvolvido por **Arthur Nunes** para otimizar os processos internos de
comunicação e agendamento de manutenções preventivas.
