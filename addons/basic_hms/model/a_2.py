#Model of Marks


class StudentMarks(models.Model):
    _name = 'student.marks'
    _rec_name = 'subjname'
   
    subjname = fields.Many2one('student.subject', string = 'Subjectname')
    mark = fields.Integer(string = 'Mark')
    branchmark =fields.Many2one('student.branch', string = "Branch")
    max_mark=fields.Integer(string="Max Marks")
    marks=fields.Many2one('student.mark',string =' ',readonly="1")
                           
    #Dynamic dropdown to display subname based on branch
    @api.onchange('branchmark')
    def _branch_onchange(self):
        res = {}
        res['domain'] = {'subjname':[('branch_id', '=', self.branchmark.id)]}
        return res