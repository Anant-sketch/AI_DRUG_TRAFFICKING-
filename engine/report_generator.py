import datetime
from typing import Dict, Any

def generate_ai_case_report(analysis_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    AI Case Summary Engine:
    Generates a formal law-enforcement Cyber Threat Intelligence Case Report
    based on threat scores, extracted entities, and XAI evidence.
    """
    if not analysis_result or analysis_result.get('status') != 'success':
        return {
            'status': 'error',
            'message': 'Invalid analysis result provided.'
        }

    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    case_id = f"CASE-INTEL-{hash(analysis_result['raw_text']) % 1000000:06d}"
    
    threat_score = analysis_result['threat_score']
    risk_level = analysis_result['risk_level']
    category = analysis_result['predicted_category']
    entities = analysis_result['entities']
    
    # 1. Executive Summary Rationale
    if risk_level in ['CRITICAL', 'HIGH']:
        summary_text = (
            f"HIGH-RISK THREAT DETECTED: The target communication exhibits strong characteristics of "
            f"illicit drug distribution and covert cyber trafficking. The system assigned a Threat Severity Score of "
            f"{threat_score}% based on NLP classification models and entity density."
        )
    elif risk_level == 'MEDIUM':
        summary_text = (
            f"SUSPICIOUS ACTIVITY FLAGGED: The target communication contains key street drug jargon or contact handles "
            f"warranting law enforcement / moderator review. Threat Severity Score: {threat_score}%."
        )
    else:
        summary_text = (
            f"LOW THREAT / BENIGN: The target communication was evaluated as legitimate medical discussion or general benign text. "
            f"Threat Severity Score: {threat_score}%."
        )

    # 2. Extracted Artifacts Summary
    handles_list = entities.get('telegram_handles', []) + entities.get('wickr_handles', []) + entities.get('session_handles', [])
    crypto_list = entities.get('bitcoin_addresses', []) + entities.get('ethereum_addresses', []) + entities.get('monero_addresses', [])
    emojis_list = entities.get('detected_emojis', [])
    keywords_list = entities.get('suspicious_keywords', [])

    # 3. Recommended Actions
    recommended_actions = []
    if risk_level == 'CRITICAL':
        recommended_actions = [
            "1. Flag user account and archive message text & IP headers for evidentiary audit.",
            "2. Submit extracted Telegram handles (@" + ", @".join(handles_list) + ") to cybercrime unit." if handles_list else "2. Trace darknet handle origin.",
            "3. Issue blockchain monitoring request for crypto wallet addresses: " + ", ".join(crypto_list) if crypto_list else "3. Monitor associated transaction logs.",
            "4. Escalate post to platform safety team for immediate takedown."
        ]
    elif risk_level == 'HIGH':
        recommended_actions = [
            "1. Place target account under automated 24-hour keyword surveillance.",
            "2. Cross-reference extracted contact handles against active darknet market registries.",
            "3. Perform manual verification of message context."
        ]
    else:
        recommended_actions = [
            "1. No immediate intervention required.",
            "2. Log communication in standard audit queue."
        ]

    # 4. Format Case Report Document
    report_markdown = f"""
================================================================================
          OFFICIAL CYBER THREAT INTELLIGENCE CASE REPORT
================================================================================
Case Reference: {case_id}
Generated Date: {now_str}
System Version: Cyber Drug Detection v2.0 (AI Major Project)

1. EXECUTIVE SUMMARY
--------------------------------------------------------------------------------
Threat Status:      {risk_level} ({threat_score}%)
Classification:     {category}
Overview:           {summary_text}

2. EXTRACTED CRIMINAL ARTIFACTS
--------------------------------------------------------------------------------
Telegram/Wickr Handles: {', '.join(handles_list) if handles_list else 'None Detected'}
Crypto Wallets (BTC/XMR):{', '.join(crypto_list) if crypto_list else 'None Detected'}
Detected Drug Emojis:   {', '.join(emojis_list) if emojis_list else 'None Detected'}
Flagged Keyword Hits:   {', '.join(keywords_list) if keywords_list else 'None Detected'}

3. ORIGINAL EVIDENTIARY TEXT
--------------------------------------------------------------------------------
"{analysis_result['raw_text']}"

4. RECOMMENDED LAW ENFORCEMENT COUNTERMEASURES
--------------------------------------------------------------------------------
{chr(10).join(recommended_actions)}
================================================================================
"""

    return {
        'status': 'success',
        'case_id': case_id,
        'timestamp': now_str,
        'threat_score': threat_score,
        'risk_level': risk_level,
        'category': category,
        'summary_text': summary_text,
        'handles': handles_list,
        'crypto_wallets': crypto_list,
        'recommended_actions': recommended_actions,
        'full_report_text': report_markdown
    }
