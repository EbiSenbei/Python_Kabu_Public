IF OBJECT_ID(N'FLD_DEF', N'U') IS NOT NULL 
DROP TABLE FLD_DEF
GO 

CREATE TABLE [dbo].[FLD_DEF]
(
    [TBL_NM]                       [nvarchar](90) NOT NULL,
    [FLD_SEQ]                      [int],
    [FLD_NM]                       [nvarchar](90) NOT NULL,
    [FLD_KNM]                      [nvarchar](180),
    [FLD_ATB]                      [nvarchar](64),
    [FLD_LEN]                      [int],
    [FLD_POS]                      [int],
    [FLD_IDX]                      [nvarchar](3),
    [NOTE_NM]                      [nvarchar](180),
    [MKUP_D]                       [datetime],
    CONSTRAINT [PK_FLD_DEF] PRIMARY KEY CLUSTERED 
(
       TBL_NM ASC, 
       FLD_NM ASC
    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
GO 


EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'物理テーブル名' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'TBL_NM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'カラムNo' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'FLD_SEQ'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'物理カラム名' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'FLD_NM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'論理カラム名' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'FLD_KNM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'データ型' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'FLD_ATB'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'桁数(整数)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'FLD_LEN'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'桁数(小数)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'FLD_POS'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'カラムインデックス' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'FLD_IDX'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'備考' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'NOTE_NM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'登録更新日時' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DEF', @level2type=N'COLUMN',@level2name=N'MKUP_D'
Go

