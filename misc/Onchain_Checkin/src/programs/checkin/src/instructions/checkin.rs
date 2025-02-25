use anchor_lang::prelude::*;

use crate::CheckinState;

#[derive(Accounts)]
pub struct Checkin<'info> {
    #[account(mut)]
    pub deployer: Signer<'info>,
    /// CHECK: account2
    pub account2: AccountInfo<'info>,
    /// CHECK: account3
    pub account3: AccountInfo<'info>,
    #[account(
        init,
        payer = deployer, 
        seeds = [b"checkin_state"],
        bump,
        space = CheckinState::INIT_SPACE
    )]
    pub checkin_state: Account<'info, CheckinState>,
    pub system_program: Program<'info, System>,
}

impl<'info> Checkin<'info> {
    pub fn checkin(&mut self) -> Result<()> { 
        self.checkin_state.flag3 = self.account3.key();
        msg!("3LDqJJCHwDBGQP9Zn5MSx");
        Ok(())
    }
}
