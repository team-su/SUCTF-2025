import fs from "fs";
import * as dotenv from "dotenv";
import * as anchor from "@coral-xyz/anchor";
import { Keypair, PublicKey, Connection } from "@solana/web3.js";
import { Checkin } from "../target/types/checkin";

dotenv.config();

async function main() {
  const connection = new Connection(process.env.DEVNET_RPC_URL);
  const deployer = Keypair.fromSecretKey(
    Buffer.from(
      JSON.parse(fs.readFileSync("./.keypair/deployer.json", "utf-8"))
    )
  );
  console.log("Deployer:", deployer.publicKey.toString());

  const provider = new anchor.AnchorProvider(
    connection,
    new anchor.Wallet(deployer),
    { commitment: "finalized" }
  );
  anchor.setProvider(provider);

  const program = anchor.workspace.Checkin as anchor.Program<Checkin>;
  const checkinState = PublicKey.findProgramAddressSync(
    [Buffer.from("checkin_state")],
    program.programId
  )[0];
  console.log("Checkin:", program.programId.toString());
  console.log("Checkin State:", checkinState.toString());

  try {
    const accountInfo = await connection.getAccountInfo(checkinState);
    if (accountInfo !== null) {
      console.log("Checkin State already exists, fetching data...");
      const state = await program.account.checkinState.fetch(checkinState);
      console.log("Checkin State Data:", {
        flag3: state.flag3.toString(),
      });
      return;
    }

    console.log("Checkin...");
    const tx = await program.methods
      .youHaveFound()
      .accountsPartial({
        deployer: deployer.publicKey,
        account2: new PublicKey("SUCTF2Q25DnchainCheckin11111111111111111111"),
        account3: new PublicKey("7Qgd9aqwprLzfS4L9KQFM3mNdG3WpjevNoCoRduXXfPS"),
        checkinState,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .signers([deployer])
      .rpc();
    console.log("Checkin Txhash:", tx);

    console.log("Waiting for transaction confirmation...");
    const latestBlockhash = await connection.getLatestBlockhash();
    await connection.confirmTransaction(
      {
        signature: tx,
        blockhash: latestBlockhash.blockhash,
        lastValidBlockHeight: latestBlockhash.lastValidBlockHeight,
      },
      "finalized"
    );

    const state = await program.account.checkinState.fetch(checkinState);
    console.log("Checkin State Data:", {
      flag3: state.flag3.toString(),
    });
  } catch (err) {
    console.error("Checkin Failed:", err);
  }
}

main().then(
  () => process.exit(),
  (err) => {
    console.error(err);
    process.exit(-1);
  }
);
