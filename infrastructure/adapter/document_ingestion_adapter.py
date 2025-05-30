import json
import requests
from typing import Dict, Any, List

from domain.port.document_ingestion_port import DocumentIngestionPort
from domain.service.document_service import DocumentService

class DocumentIngestionAdapter(DocumentIngestionPort):
    def __init__(self, document_service: DocumentService):
        self.document_service = document_service

    def ingest_user_specific_documents(self, user_id: str, user_info: Dict[str, Any]) -> List[str]:
        """Ingest CAF-specific documents for a user"""
        documents_to_ingest = [
            {
                "title": f"Attestation de droits - {user_info.get('first_name', '')} {user_info.get('last_name', '')}",
                "content": self._generate_attestation_content(user_info),
                "document_type": "attestation_droits",
                "source_service": "caf_attestation_service"
            },
            {
                "title": "Guide des prestations CAF 2024",
                "content": self._get_prestations_guide(),
                "document_type": "guide_prestations",
                "source_service": "caf_info_service"
            },
            {
                "title": "Procédures de déclaration trimestrielle",
                "content": self._get_declaration_procedures(),
                "document_type": "procedures",
                "source_service": "caf_procedure_service"
            }
        ]
        
        ingested_ids = []
        for doc in documents_to_ingest:
            doc_id = self.document_service.process_document_with_chunks(
                title=doc["title"],
                content=doc["content"],
                document_type=doc["document_type"],
                source_service=doc["source_service"],
                metadata={"user_id": user_id, "ingestion_source": "automated"}
            )
            ingested_ids.append(doc_id)
        
        return ingested_ids

    def ingest_from_external_source(self, source_id: str, source_config: Dict[str, Any]) -> List[str]:
        """Ingest documents from external API"""
        try:
            api_url = source_config.get("api_url")
            headers = source_config.get("headers", {})
            
            response = requests.get(api_url, headers=headers)
            response.raise_for_status()
            
            external_docs = response.json()
            ingested_ids = []
            
            for doc_data in external_docs:
                doc_id = self.document_service.process_document_with_chunks(
                    title=doc_data.get("title", "External Document"),
                    content=doc_data.get("content", ""),
                    document_type=doc_data.get("type", "external"),
                    source_service=source_id,
                    metadata={"external_id": doc_data.get("id"), "source_config": source_config}
                )
                ingested_ids.append(doc_id)
            
            return ingested_ids
            
        except Exception as e:
            print(f"Error ingesting from external source: {e}")
            return []

    def _generate_attestation_content(self, user_info: Dict[str, Any]) -> str:
        return f"""
ATTESTATION DE DROITS CAF

Allocataire: {user_info.get('first_name', '')} {user_info.get('last_name', '')}
Numéro allocataire: {user_info.get('id_number', '')}
Date de naissance: {user_info.get('birth_date', '')}

PRESTATIONS EN COURS:
- Allocations Familiales: Selon le nombre d'enfants à charge
- Aide Personnalisée au Logement (APL): Selon votre situation locative
- Prime d'activité: Complément de revenu pour les travailleurs

CONDITIONS D'ÉLIGIBILITÉ:
- Résidence en France
- Déclaration trimestrielle à jour
- Justificatifs de revenus fournis

Pour toute question concernant vos droits, contactez votre CAF départementale.
        """.strip()

    def _get_prestations_guide(self) -> str:
        return """
GUIDE DES PRESTATIONS CAF 2024

ALLOCATIONS FAMILIALES:
- À partir du 2ème enfant
- Montant: 141,99€ pour 2 enfants, 323,92€ pour 3 enfants
- Majoration à partir de 14 ans

AIDE PERSONNALISÉE AU LOGEMENT (APL):
- Aide pour réduire le montant du loyer
- Montant selon revenus, composition familiale et zone géographique
- Demande via le site caf.fr

PRIME D'ACTIVITÉ:
- Complément de revenus pour les travailleurs
- Conditions: revenus d'activité, ressources limitées
- Simulation disponible sur caf.fr

RSA (REVENU DE SOLIDARITÉ ACTIVE):
- Aide pour les personnes sans emploi ou avec revenus limités
- Montant forfaitaire: 607,75€ pour une personne seule
- Obligation d'insertion professionnelle

AIDE AU LOGEMENT SOCIALE (ALS):
- Pour logements non conventionnés
- Complément à l'APL quand celle-ci n'est pas applicable

ALLOCATION ADULTE HANDICAPÉ (AAH):
- Pour personnes en situation de handicap
- Montant: jusqu'à 971,37€
- Évaluation par MDPH requise
        """.strip()

    def _get_declaration_procedures(self) -> str:
        return """
PROCÉDURES DE DÉCLARATION TRIMESTRIELLE

PÉRIODICITÉ:
- Déclaration obligatoire tous les 3 mois
- Dates limites: 31 janvier, 30 avril, 31 juillet, 31 octobre

ÉLÉMENTS À DÉCLARER:
- Revenus d'activité salariée ou non salariée
- Revenus de remplacement (chômage, maladie)
- Autres ressources du foyer
- Changements de situation familiale

MODALITÉS:
1. Connexion sur caf.fr avec identifiants
2. Rubrique "Mes démarches" > "Déclarer mes ressources"
3. Saisie des montants pour chaque mois du trimestre
4. Validation et envoi

DOCUMENTS NÉCESSAIRES:
- Bulletins de paie
- Attestations Pôle emploi
- Relevés bancaires si revenus variables
- Justificatifs de pensions/rentes

CONSÉQUENCES DU RETARD:
- Suspension des prestations
- Récupération des indus
- Pénalités possibles

AIDE À LA DÉCLARATION:
- Simulation en ligne
- Télé-services personnalisés
- Accueil téléphonique: 3230
        """.strip() 