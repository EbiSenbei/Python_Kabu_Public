IF OBJECT_ID(N'FLD_DIC', N'U') IS NOT NULL 
DROP TABLE FLD_DIC
GO 

CREATE TABLE [dbo].[FLD_DIC]
(
    [FLD_NM]                       [nvarchar](90) NOT NULL,
    [FLD_KNM]                      [nvarchar](90),
    [FLD_ATB]                      [nvarchar](180),
    [FLD_LEN]                      [int],
    [FLD_POS]                      [int],
    [NOTE_NM]                      [nvarchar](180),
    [MKUP_D]                       [datetime],
    CONSTRAINT [PK_FLD_DIC] PRIMARY KEY CLUSTERED 
(
       FLD_NM ASC
    )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
GO 


EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'�����J������' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DIC', @level2type=N'COLUMN',@level2name=N'FLD_NM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'�_���J������' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DIC', @level2type=N'COLUMN',@level2name=N'FLD_KNM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'�f�[�^�^' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DIC', @level2type=N'COLUMN',@level2name=N'FLD_ATB'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'����(����)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DIC', @level2type=N'COLUMN',@level2name=N'FLD_LEN'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'����(����)' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DIC', @level2type=N'COLUMN',@level2name=N'FLD_POS'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'���l' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DIC', @level2type=N'COLUMN',@level2name=N'NOTE_NM'
Go
EXEC sys.sp_addextendedproperty @name=N'MS_Description', @value=N'�o�^�X�V����' , @level0type=N'SCHEMA',@level0name=N'dbo', @level1type=N'TABLE',@level1name=N'FLD_DIC', @level2type=N'COLUMN',@level2name=N'MKUP_D'
Go

