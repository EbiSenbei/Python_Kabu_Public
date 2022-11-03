IF OBJECT_ID(N'TBL_DEF', N'U') IS NOT NULL 
DROP TABLE TBL_DEF
GO 

CREATE TABLE [dbo].[TBL_DEF]
(
    [TBL_NM]                       [nvarchar](90) NOT NULL,
    [TBL_KNM]                      [nvarchar](180) DEFAULT '',
    [NOTE_NM]                      [nvarchar](180),
    [MKUP_D]                       [datetime],
    CONSTRAINT [PK_TBL_DEF] PRIMARY KEY CLUSTERED 
(
       TBL_NM ASC
    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
GO 


EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'物理テーブル名' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'TBL_DEF', @level2type=N'COLUMN',@level2name=N'TBL_NM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'論理テーブル名' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'TBL_DEF', @level2type=N'COLUMN',@level2name=N'TBL_KNM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'備考' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'TBL_DEF', @level2type=N'COLUMN',@level2name=N'NOTE_NM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'登録更新日時' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'TBL_DEF', @level2type=N'COLUMN',@level2name=N'MKUP_D'
Go

