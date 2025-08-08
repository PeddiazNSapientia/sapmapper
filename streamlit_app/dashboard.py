import streamlit as st
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

API_URL = "http://localhost:8052"

st.title("SAP ↔ Salesforce Mapper")

# # Función auxiliar para obtener JSON seguro
def safe_get_json(url):
    try:
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        st.error(f"Error HTTP: {http_err}")
    except requests.exceptions.RequestException as req_err:
        st.error(f"Error de conexión: {req_err}")
    except ValueError as json_err:
        st.error(f"Respuesta no es JSON válido: {json_err}")
    except Exception as e:
        st.error(f"Error inesperado: {e}")
    return {}

# # Obtener entidades
entities_data = safe_get_json(f"{API_URL}/entities")
entities = entities_data.get("entities", [])
# response = requests.get("http://localhost:8052/entities")
# st.write(response.json())


selected_entity = st.selectbox("Selecciona una entidad SAP", entities)

if selected_entity:
    # Obtener campos de la entidad
    fields_data = safe_get_json(f"{API_URL}/entities/{selected_entity}")
    fields = fields_data.get("fields", [])

    sap_field = st.selectbox("Campo SAP", fields)
    salesforce_field = st.text_input("Campo Salesforce")

    if st.button("Guardar mapeo"):
        payload = {
            "sap_entity": selected_entity,
            "sap_field": sap_field,
            "salesforce_field": salesforce_field
        }
        try:
            res = requests.post(f"{API_URL}/map/salesforce", json=payload, verify=False)
            res.raise_for_status()
            st.success("Mapeo guardado")
        except requests.exceptions.RequestException as e:
            st.error(f"Error al guardar el mapeo: {e}")

    st.subheader("Mapeos existentes")
    mappings_data = safe_get_json(f"{API_URL}/map/salesforce/{selected_entity}")
    mappings = mappings_data if isinstance(mappings_data, list) else []

    for m in mappings:
        st.write(f"{m.get('sap_field', '¿?')} → {m.get('salesforce_field', '¿?')}")
