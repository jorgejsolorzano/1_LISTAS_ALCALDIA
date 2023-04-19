#Model of Marklist

class StudentMarkList(models.Model):
    _name = 'student.mark'
    _rec_name = 'student_id'

    student_id = fields.Many2one('student.student',
        string = 'StudentName')
    branch = fields.Many2one('student.branch',related='student_id.branchname',
        string = 'Branch Name')
    # Setting Related field
    #age = fields.Integer(related='student_id.age',string='Age')
    '''
    total = fields.Integer(string = 'Total Mark', store = True,
        compute = '_compute_total')'''
    subname = fields.One2many('student.marks', 'marks',
        string = 'Subjectwise Marks')       
    hide_inv_button = fields.Boolean(copy = False, default = True)
    state = fields.Selection([('confirmed', 'Confirm'),
                            ('cancelled', 'Cancel')],
                            string = 'Status', readonly = True,
                            copy = False, index = True,
                            track_visibility = 'onchange')
    max_marks =fields.Float(string="max_marks",
                                     compute="_compute_totalmark",
                                     store=True)
    total_mark = fields.Float("Total Mark",
                                     compute="_compute_totalmark",
                                     store=True)
    percent_mark = fields.Float("Percentage Mark",
                                     compute="_compute_percentmark",
                                     store=True)
                                                                                                                                                                 
    #method to compute total mark
    @api.multi
    @api.depends("subname")
    def _compute_totalmark(self):
        self.total_mark=0
        self.max_marks=0
        for rec in self.subname:
            self.total_mark = self.total_mark+rec.mark
            self.max_marks+=rec.max_mark
   
    #method to compute percentage mark
    @api.multi
    @api.depends("total_mark","max_marks")
    def _compute_percentmark(self):
        for rec in self:
            if rec.max_marks>0:
                rec.percent_mark = (rec.total_mark/rec.max_marks)*100    