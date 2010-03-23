import virtualCell

sol = virtualCell.Solution(1000000)
sol.addCell(1000.0)

sol.cells[0].DNA = 'CCCBBCDBAA'
#sol.cells[0].DNA = 'BACBDDAABACBDDAABAAADDDABBADDDAABCABDDAABABDBCAA'

sol.cells[0].interpretDNA()
sol.cells[0].outputProteins()
