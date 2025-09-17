from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField, HiddenField
from wtforms.validators import DataRequired, Length, Optional, URL

class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired(), Length(min=5, max=200)])
    content = TextAreaField('内容', validators=[DataRequired(), Length(min=10)])
    summary = TextAreaField('摘要', validators=[Optional(), Length(max=500)])
    featured_image = StringField('特色图片URL', validators=[Optional(), URL()])
    tags = StringField('标签（用逗号分隔）', validators=[Optional()])
    is_published = BooleanField('立即发布')
    submit = SubmitField('保存文章')

class CommentForm(FlaskForm):
    content = TextAreaField('评论内容', validators=[DataRequired(), Length(min=2, max=1000)])
    parent_id = HiddenField('回复评论ID')
    submit = SubmitField('发表评论')