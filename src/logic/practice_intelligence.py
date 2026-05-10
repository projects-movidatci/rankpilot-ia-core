def get_practice_rules(practice_area: str, directory_type: str) -> str:
    """Returns the universal evaluation logic based on the practice area."""
    practice = str(practice_area).upper()
    
    if directory_type == "Chambers":
        if "M&A" in practice or "CORPORATE" in practice:
            return "CHAMBERS M&A: Focus heavily on transactional complexity, cross-border coordination, and 'bet-the-company' mandates. Volume alone is not enough; highlight the strategic role of the firm in structuring the deals."
        elif "BANKING" in practice or "FINANCE" in practice:
            return "CHAMBERS BANKING: Prioritize the sophistication of collateral structures, regulatory navigation, and lender-side/borrower-side dynamics. Highlight dual-law complexities if applicable."
        elif "DISPUTES" in practice or "LITIGATION" in practice or "ARBITRATION" in practice:
            return "CHAMBERS DISPUTES: Emphasize market-shaping precedents, extreme financial risk, and appellate/supreme court victories. Exclude routine debt collection or low-risk litigation."
        elif "TAX" in practice:
            return "CHAMBERS TAX: Focus on complex tax structuring, major audits, and transfer pricing. Differentiate between advisory and controversy."
        elif "FINTECH" in practice:
            return "CHAMBERS FINTECH: Highlight regulatory pioneer work, sandbox approvals, and novel digital asset structuring."
        else:
            return f"CHAMBERS STANDARD: Focus on complex matters and individual partner expertise in {practice_area}."
            
    elif directory_type == "Legal500":
        if "M&A" in practice or "CORPORATE" in practice:
            return "LEGAL 500 M&A: Highlight absolute market share, total deal volume, and the breadth of the team. Show that Next-Gen partners and senior associates are leading significant transactions."
        elif "BANKING" in practice or "FINANCE" in practice:
            return "LEGAL 500 BANKING: Focus on the volume of credit facilities, diversity of the lender portfolio, and team depth."
        elif "DISPUTES" in practice:
            return "LEGAL 500 DISPUTES: Showcase a high volume of active cases, diverse industry representation, and bench strength across different judicial levels."
        else:
            return f"LEGAL 500 STANDARD: Emphasize team depth, volume of work, and client retention in {practice_area}."
            
    return "Follow standard legal prose."